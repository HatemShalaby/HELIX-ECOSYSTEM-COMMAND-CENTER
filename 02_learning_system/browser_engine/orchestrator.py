import sys
import os
import threading
import time
import logging
import requests
from pathlib import Path
from playwright.sync_api import sync_playwright

# Force Python to find modules in the current directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from education_engine import create_lesson
from quiz_automator import process_lessons
from renderer import render_to_html, SELECTORS
from feedback_handler import app
from path_config import LEARNING_SYS_DIR, LESSONS_DIR, RECORDS_DIR

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("orchestrator")

def start_feedback_server():
    """Starts the Flask feedback server in a daemon thread."""
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    
    logger.info("Starting background feedback server on port 5000...")
    flask_thread = threading.Thread(
        target=lambda: app.run(port=5000, debug=False, use_reloader=False),
        daemon=True
    )
    flask_thread.start()
    time.sleep(1.5)

def run_diagnostic_cleanup():
    """Runs blueprint diagnostic routine to clean filesystem and check for staging files."""
    logger.info("Running diagnostic routine cleanup...")
    search_dirs = [LESSONS_DIR, RECORDS_DIR, Path(__file__).parent]
    purged_count = 0
    for directory in search_dirs:
        if directory.exists():
            for partial_file in directory.glob("*-partial*"):
                try:
                    if partial_file.is_file():
                        partial_file.unlink()
                    elif partial_file.is_dir():
                        import shutil
                        shutil.rmtree(partial_file)
                    purged_count += 1
                    logger.info(f"Purged partial staging file: {partial_file.name}")
                except Exception as e:
                    logger.warning(f"Could not purge staging item {partial_file}: {e}")
                    
    if purged_count > 0:
        logger.info(f"Successfully purged {purged_count} partial staging items.")
    else:
        logger.info("No partial files or corrupted staging items found. Filesystem clean.")

def run_orchestration(topic, is_mock_test=False):
    """
    Executes the full automated learning loop.
    """
    print(f"\n==================================================")
    print(f"🎓 Starting Learning System: {topic}")
    print(f"==================================================\n")
    
    # 1. Diagnostic cleanup
    run_diagnostic_cleanup()

    # 2. Generate lesson and quiz (sequential to avoid VRAM overload)
    logger.info(f"Step 1/4: Generating lesson content via LLM...")
    lesson_path = create_lesson(topic)
    logger.info(f"Lesson saved to: {lesson_path}")
    
    logger.info(f"Step 2/4: Processing & refining quizzes...")
    process_lessons()
    
    logger.info(f"Step 3/4: Compiling Markdown to interactive HTML...")
    html_path = render_to_html(topic)
    if not html_path or not html_path.exists():
        logger.error("Failed to render HTML file.")
        return False
        
    logger.info(f"HTML output ready at: {html_path}")
    
    # Start the Flask background server
    start_feedback_server()
    
    file_url = html_path.absolute().as_uri()

    if not is_mock_test:
        print(f"\n==================================================")
        print(f"🌐 Quiz ready: {file_url}")
        print("Open the URL above to complete the quiz in your browser.")
        print("Press Ctrl+C to stop the feedback server.")
        print(f"==================================================\n")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Feedback server stopped by user.")
            return True

    logger.info(f"Step 4/4: Initializing headless Playwright engine...")
    
    session_success = False
    
    with sync_playwright() as p:
        logger.info("Launching chromium driver (headless=True)...")
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        # RESOURCE THROTTLING: Block heavy assets
        def intercept_route(route):
            if route.request.resource_type in ["image", "media", "font", "stylesheet"] and not route.request.url.startswith("file:"):
                logger.debug(f"Throttled asset: {route.request.url}")
                route.abort()
            else:
                route.continue_()
                
        page.route("**/*", intercept_route)
        page.goto(file_url)
        
        # Wait for the progress indicator to load
        page.wait_for_selector(SELECTORS["progress_indicator"])
        progress_text = page.locator(SELECTORS["progress_indicator"]).text_content()
        logger.info(f"Interactive state parsed: {progress_text}")
        
        # Main quiz interaction loop
        while True:
            # Check if quiz is completed by looking for the "Quiz Complete!" message
            # The completion screen replaces the container's inner HTML.
            if page.locator("text=Quiz Complete!").count() > 0:
                logger.info("Quiz completion detected. Exiting loop.")
                break
            
            # Also check if the "interactive-quiz-container" no longer contains the question
            # (fallback in case text detection is delayed)
            container = page.locator("#interactive-quiz-container")
            if container.count() > 0:
                inner = container.inner_html()
                if "Quiz Complete!" in inner:
                    logger.info("Quiz completion detected via container inner HTML.")
                    break
            
            # Now read the current question text
            try:
                current_q = page.locator(SELECTORS["question_text"]).text_content(timeout=5000)
            except Exception:
                # If we can't read the question, assume quiz ended
                logger.warning("Could not read question text – assuming quiz finished.")
                break
            
            print(f"\n--------------------------------------------------")
            print(f"📖 {progress_text}")  # The progress text from earlier (Question X of Y)
            print(f"❓ Question: {current_q}")
            
            # Get answer
            if is_mock_test:
                answer = f"This is an automated mock response. {topic} relies on robust dynamic modular coordination and resource-bounded optimization."
                print(f"✍️ [Automated Answer Entered]: {answer}")
                time.sleep(1)
            else:
                try:
                    answer = input("✍️ Enter your detailed answer: ").strip()
                    while not answer:
                        answer = input("Answer cannot be empty. Enter your detailed answer: ").strip()
                except KeyboardInterrupt:
                    logger.info("Session interrupted by user.")
                    break
            
            # Submit answer via Playwright
            page.fill(SELECTORS["answer_input"], answer)
            page.click(SELECTORS["submit_button"])
            
            # Wait for feedback to appear
            page.wait_for_selector(SELECTORS["feedback_area"], state="visible")
            
            evaluation = page.locator(SELECTORS["evaluation_text"]).text_content()
            print(f"\n💡 [Tutor Evaluation Feedback]:")
            print(evaluation)
            print(f"--------------------------------------------------\n")
            
            # Move to next question if possible
            next_btn = page.locator(SELECTORS["next_button"])
            if next_btn.count() > 0 and next_btn.is_visible():
                next_btn.click()
                time.sleep(0.5)
            else:
                # No next button – quiz finished
                logger.info("No next button visible. Quiz completed.")
                break
        
        # Brief pause to ensure final logging completes
        time.sleep(1)
        browser.close()
        session_success = True

    try:
        requests.post("http://localhost:5000/save_session", timeout=10)
    except Exception as e:
        logger.error(f"Failed to save mock session: {e}")
        
    print(f"\n==================================================")
    print(f"✅ Session Complete. Cleanly exited and state saved.")
    print(f"==================================================\n")
    return session_success

if __name__ == "__main__":
    is_test = "--test" in sys.argv or "-t" in sys.argv
    # Clean sys.argv to extract topic
    args = [a for a in sys.argv if not a.startswith("-")]
    
    if len(args) < 2:
        topic = "Machine Learning"
    else:
        topic = args[1]
        
    run_orchestration(topic, is_mock_test=is_test)