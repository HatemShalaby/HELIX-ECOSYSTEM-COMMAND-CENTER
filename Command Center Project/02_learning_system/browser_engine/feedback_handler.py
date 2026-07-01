import os
import sys
import logging
import json
from pathlib import Path
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from education_engine import grade_answer
from path_config import RECORDS_DIR, MEMORY_DIR, TRACKER_PATH, LESSONS_DIR

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("feedback_handler")

app = Flask(__name__)
CORS(app)

# In-memory list to accumulate active session data before explicit save/discard
session_answers = []
current_quiz_questions = {}

@app.route('/submit', methods=['POST'])
def handle_feedback():
    try:
        data = request.json or {}
        topic = data.get('topic', 'General Learning')
        question = data.get('question', 'Unknown Question')
        answer = data.get('content', '')
        q_idx = data.get('question_index', 1)
        total_qs = data.get('total_questions', 1)
        
        logger.info(f"Received answer for '{topic}' Question {q_idx}/{total_qs}")
        
        # Identify the most recent lesson file content to use for grading context
        lesson_content = "No lesson content found."
        lesson_files = list(LESSONS_DIR.glob("*.md"))
        if lesson_files:
            latest_file = max(lesson_files, key=lambda f: f.stat().st_mtime)
            with open(latest_file, "r", encoding="utf-8") as f:
                lesson_content = f.read()

        # Grade
        evaluation = grade_answer(answer, lesson_content)
        
        session_answers.append({
            "topic": topic,
            "index": q_idx,
            "total_questions": total_qs,
            "question": question,
            "answer": answer,
            "evaluation": evaluation
        })

        if topic not in current_quiz_questions:
            current_quiz_questions[topic] = []
        if question not in current_quiz_questions[topic]:
            current_quiz_questions[topic].append(question)
            
        return jsonify({"evaluation": evaluation}), 200
        
    except Exception as e:
        logger.error(f"Error in feedback submission: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route('/save_session', methods=['POST'])
def save_session():
    try:
        if not session_answers:
            return jsonify({"message": "No session answers to save."}), 200

        RECORDS_DIR.mkdir(parents=True, exist_ok=True)
        MEMORY_DIR.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        timestamp_filename = datetime.now().strftime("%Y%m%d_%H%M%S")
        topic = session_answers[0].get("topic", "General Learning")
        topic_clean = topic.replace(' ', '_').lower()
        record_file = RECORDS_DIR / f"session_{topic_clean}_{timestamp_filename}.md"

        logger.info(f"Writing complete session record to: {record_file}")

        lines = [
            f"# Learning Session Record: {topic}",
            f"- **Date/Time:** {timestamp}",
            f"- **Status:** Completed",
            "\n## Quiz Evaluations"
        ]

        for entry in session_answers:
            lines.append(f"\n### Question {entry['index']}: {entry['question']}")
            lines.append(f"- **User Answer:** {entry['answer']}")
            lines.append(f"- **Tutor Evaluation:** {entry['evaluation']}")

        with open(record_file, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        with open(TRACKER_PATH, "a", encoding="utf-8") as f:
            for entry in session_answers:
                f.write(f"\n\n## Topic: {entry['topic']}\n### Question {entry['index']}: {entry['question']}\n### Answer:\n{entry['answer']}\n### Evaluation:\n{entry['evaluation']}\n")

        metacognitive_log_path = MEMORY_DIR / "metacognitive_log.json"
        if metacognitive_log_path.exists():
            with open(metacognitive_log_path, "r", encoding="utf-8") as f:
                try:
                    metacognitive_log = json.load(f)
                except json.JSONDecodeError:
                    metacognitive_log = []
        else:
            metacognitive_log = []

        metacognitive_log.append({
            "timestamp": timestamp,
            "topic": topic,
            "record_file": str(record_file),
            "answers_count": len(session_answers)
        })

        with open(metacognitive_log_path, "w", encoding="utf-8") as f:
            json.dump(metacognitive_log, f, indent=2)

        session_answers.clear()

        return jsonify({"message": "Session saved successfully."}), 200
    except Exception as e:
        logger.error(f"Failed to save session: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route('/discard_session', methods=['POST'])
def discard_session():
    session_answers.clear()
    return jsonify({"message": "Session discarded successfully."}), 200

@app.route('/api/questions', methods=['GET'])
def get_questions():
    topic = request.args.get('topic', 'General Learning')
    questions = current_quiz_questions.get(topic, [])
    return jsonify({"topic": topic, "questions": questions}), 200

if __name__ == '__main__':
    logger.info("Starting local feedback handler on port 5000...")
    app.run(port=5000)
