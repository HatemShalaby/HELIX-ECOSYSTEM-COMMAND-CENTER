import logging
from pathlib import Path
from quiz_generator import format_quiz
from model_registry import get_model
from path_config import LESSONS_DIR

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("quiz_automator")

def generate_quiz_with_ai(content):
    model = get_model("default_quiz_model")
    prompt = f"Generate 3 challenging quiz questions based on the following content:\n\n{content}\n\nFormat as a markdown list."
    
    if model == "stub-model":
        logger.warning("No local model available for quiz generation. Falling back to default questions.")
        return get_stub_quiz_questions()
        
    try:
        import ollama
        logger.info(f"Generating quiz using model: {model}")
        response = ollama.chat(model=model, messages=[
            {'role': 'system', 'content': 'You are a technical tutor. Provide concise, clear answers.'},
            {'role': 'user', 'content': prompt},
        ])
        return response['message']['content']
    except Exception as e:
        logger.error(f"Quiz generation with LLM failed: {e}. Falling back to default questions.")
        return get_stub_quiz_questions()

def get_stub_quiz_questions():
    return """
1. **Question 1**: Explain the primary design pattern showcased in the lesson and its main benefits.
   *Answer: Discuss the structure, separation of concerns, and modularity.*
2. **Question 2**: What is a critical security vulnerability or failure point to look out for with this concept?
   *Answer: Mention input validation, unauthorized access, and lack of rate-limiting.*
3. **Question 3**: How should resource limits and clean shutdown routines be handled under production workloads?
   *Answer: Mention timeouts, resource-throttling, blocking heavy media, and sequential task queues.*
"""

def process_lessons():
    for lesson_file in LESSONS_DIR.glob("*.md"):
        content = lesson_file.read_text(encoding="utf-8")
        
        # Guard clause: Skip if quiz section exists and isn't a placeholder
        if "## Quiz" in content and "*No quiz provided*" not in content and "Q1:" not in content:
            continue
            
        logger.info(f"Generating quiz for {lesson_file.name}...")
        quiz_data = generate_quiz_with_ai(content)
        
        # Integration: Split content and append new quiz
        if "## Quiz" in content:
            base_content = content.split("## Quiz")[0]
        else:
            base_content = content
            
        updated_content = base_content.strip() + "\n\n" + format_quiz(quiz_data)
        lesson_file.write_text(updated_content, encoding="utf-8")
        logger.info(f"Successfully updated {lesson_file.name}")

if __name__ == "__main__":
    process_lessons()
