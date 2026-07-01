import markdown
from pathlib import Path
from path_config import LESSONS_DIR

# Selector Map for DOM targeting - makes it robust against DOM changes
SELECTORS = {
    "lesson_content": ".lesson-content",
    "question_text": "#current-question-text",
    "answer_input": "#ans",
    "submit_button": "#submitBtn",
    "feedback_area": "#feedback-area",
    "next_button": "#nextBtn",
    "status_message": "#msg",
    "progress_indicator": "#quiz-progress",
    "evaluation_text": "#evaluation-text"
}

def render_to_html(topic):
    topic_clean = topic.replace(' ', '_').lower()
    md_file = LESSONS_DIR / f"{topic_clean}.md"
    html_file = md_file.with_suffix(".html")
    
    with open(md_file, "r", encoding="utf-8") as f:
        md_content = f.read()

    sanitized_lines = []
    skip_answer_section = False
    previous_line_was_question = False
    for line in md_content.splitlines():
        stripped = line.strip()
        normalized = stripped.lower()

        if normalized in {"## answers", "## answer key", "### answers", "### answer key", "answer key", "answers"}:
            skip_answer_section = True
            previous_line_was_question = False
            continue

        if skip_answer_section:
            if stripped.startswith("#") and "answer" not in normalized:
                skip_answer_section = False
            else:
                continue

        if normalized.startswith(("answer:", "correct:")):
            previous_line_was_question = False
            continue

        if previous_line_was_question and stripped.startswith("A. "):
            previous_line_was_question = False
            continue

        sanitized_lines.append(line)
        previous_line_was_question = stripped.endswith("?")
        
    md_content = "\n".join(sanitized_lines)
    
    rendered_markdown = markdown.markdown(md_content, extensions=['fenced_code', 'tables'])
    
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Learning System: {topic}</title>
    <style>
        body {{ background-color: #121212; color: #e0e0e0; font-family: 'Segoe UI', sans-serif; line-height: 1.6; padding: 40px; margin: 0; }}
        .focus-container {{ max-width: 800px; margin: auto; }}
        .card {{ background: #1e1e1e; padding: 40px; border-radius: 16px; border: 1px solid #333; margin-bottom: 20px; }}
        h1 {{ color: #00e676; margin-top: 0; }}
        h2 {{ color: #00b0ff; border-bottom: 1px solid #333; padding-bottom: 10px; }}
        code {{ background: #000; padding: 2px 6px; color: #ffeb3b; font-family: 'Consolas', monospace; border-radius: 4px; }}
        pre code {{ display: block; padding: 15px; overflow-x: auto; }}
        textarea {{ width: 100%; height: 120px; background: #2c2c2c; color: white; border: 1px solid #444; border-radius: 8px; padding: 15px; box-sizing: border-box; font-size: 14px; resize: vertical; }}
        button {{ background: #00e676; color: #000; border: none; padding: 12px 24px; border-radius: 8px; font-weight: bold; cursor: pointer; margin-top: 10px; font-size: 14px; transition: background 0.2s; }}
        button:hover {{ background: #00c853; }}
        button:disabled {{ background: #555; color: #888; cursor: not-allowed; }}
        .success-msg {{ display: none; color: #00e676; margin-top: 10px; font-weight: bold; }}
        .quiz-section {{ border-top: 2px dashed #444; padding-top: 20px; }}
        .quiz-card {{ background: #1a237e; border: 1px solid #3f51b5; padding: 25px; border-radius: 12px; margin-top: 20px; }}
        .feedback {{ background: #263238; border-left: 5px solid #00e676; padding: 15px; margin-top: 15px; border-radius: 4px; display: none; }}
        .progress {{ font-size: 14px; color: #b0bec5; font-weight: bold; margin-bottom: 10px; }}
    </style>
</head>
<body>
    <div class="focus-container">
        <!-- Lesson Content Card -->
        <div class="card lesson-content">
            {rendered_markdown}
        </div>
        
        <!-- Interactive Quiz Card -->
        <div class="card quiz-section" id="interactive-quiz-container">
            <h2>Interactive Quiz</h2>
            <div class="quiz-card">
                <div class="progress" id="quiz-progress">Question 1 of ...</div>
                <h3 id="current-question-text">Loading question...</h3>
                <textarea id="ans" placeholder="Type your detailed response here..."></textarea>
                <div>
                    <button id="submitBtn" onclick="submitAnswer()">Submit Answer</button>
                    <button id="nextBtn" onclick="nextQuestion()" style="display: none; background: #00b0ff; color: #000;">Next Question</button>
                </div>
                <p id="msg" class="success-msg">✓ Evaluation received and logged.</p>
                <div class="feedback" id="feedback-area">
                    <strong>Tutor Evaluation:</strong>
                    <p id="evaluation-text"></p>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Track quiz state
        let questions = [];
        let currentIndex = 0;
        let answersLogged = [];
        const quizTopic = "{topic}";

        document.addEventListener("DOMContentLoaded", async () => {{
            await loadQuizQuestions();
            displayQuestion();
        }});

        async function loadQuizQuestions() {{
            const response = await fetch(`http://localhost:5000/api/questions?topic=${{encodeURIComponent(quizTopic)}}`);
            const data = await response.json();
            questions = Array.isArray(data.questions) ? data.questions : [];
        }}

        function displayQuestion() {{
            if (currentIndex < questions.length) {{
                document.getElementById('quiz-progress').textContent = `Question ${{currentIndex + 1}} of ${{questions.length}}`;
                document.getElementById('current-question-text').textContent = questions[currentIndex];
                document.getElementById('ans').value = '';
                document.getElementById('ans').disabled = false;
                document.getElementById('submitBtn').disabled = false;
                document.getElementById('nextBtn').style.display = 'none';
                document.getElementById('feedback-area').style.display = 'none';
                document.getElementById('msg').style.display = 'none';
            }} else {{
                // Quiz completed
                document.getElementById('interactive-quiz-container').innerHTML = `
                    <h2>Interactive Quiz Complete!</h2>
                    <div class="quiz-card" style="background: #1b5e20; border-color: #4caf50;">
                        <h3>🎉 Well done!</h3>
                        <p>You have successfully completed the quiz session for <strong>{topic}</strong>.</p>
                        <p>All evaluations have been successfully compiled and saved to learning records.</p>
                    </div>
                `;
            }}
        }}

        async function submitAnswer() {{
            const answerVal = document.getElementById('ans').value.trim();
            if (!answerVal) {{
                alert("Please write an answer before submitting.");
                return;
            }}
            
            const btn = document.getElementById('submitBtn');
            btn.disabled = true;
            document.getElementById('ans').disabled = true;
            
            const questionText = questions[currentIndex];
            
            try {{
                const response = await fetch('http://localhost:5000/submit', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{
                        topic: "{topic}",
                        question: questionText,
                        content: answerVal,
                        question_index: currentIndex + 1,
                        total_questions: questions.length
                    }})
                }});
                
                if (response.ok) {{
                    const resData = await response.json();
                    document.getElementById('msg').style.display = 'block';
                    document.getElementById('evaluation-text').textContent = resData.evaluation || 'No details provided';
                    document.getElementById('feedback-area').style.display = 'block';
                    document.getElementById('nextBtn').style.display = 'inline-block';
                }} else {{
                    alert("Submission failed. Server returned error.");
                    btn.disabled = false;
                    document.getElementById('ans').disabled = false;
                }}
            }} catch (e) {{
                console.error(e);
                alert("Backend server not responding. Ensure orchestrator has started the feedback handler.");
                btn.disabled = false;
                document.getElementById('ans').disabled = false;
            }}
        }}

        function nextQuestion() {{
            currentIndex++;
            displayQuestion();
        }}
    </script>
</body>
</html>
"""
    html_file.write_text(html_template, encoding="utf-8")
    return html_file
