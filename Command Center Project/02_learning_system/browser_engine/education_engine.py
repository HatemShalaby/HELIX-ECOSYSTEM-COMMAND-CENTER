import logging
import time
import sys
from pathlib import Path
from model_registry import get_model
from path_config import LESSONS_DIR
import ollama

logger = logging.getLogger("education_engine")

def create_lesson(topic):
    model_name = get_model("default_lesson_model")
    logger.info(f"Generating lesson for '{topic}' using model: {model_name}")

    prompt = f"""Create a detailed, structured Markdown lesson about "{topic}". Include:
1. Introduction
2. Key Concepts
3. Practical Examples
4. Quiz: 3 multiple-choice questions with correct answers indicated.

Format as valid Markdown without wrapping in code fences."""

    try:
        response = ollama.chat(
            model=model_name,
            messages=[{"role": "user", "content": prompt}]
        )
        content = response['message']['content']
    except Exception as e:
        logger.error(f"Failed to generate lesson: {e}")
        raise

    topic_clean = topic.replace(' ', '_').lower()
    LESSONS_DIR.mkdir(parents=True, exist_ok=True)
    md_path = LESSONS_DIR / f"{topic_clean}.md"
    md_path.write_text(content, encoding="utf-8")

    return md_path

def grade_answer(answer: str, lesson_content: str) -> str:
    model_name = get_model("default_grading_model")

    system_prompt = """You are a strict academic grader. Evaluate the answer against the lesson content.
Return your response in this exact format: Score: X | Feedback: [your feedback]
Rules: If the answer does not address the question topic, assign Score: 0.
Do not award points for generic or unrelated statements.
Score range is 0-100."""

    prompt = f"""Lesson content:
{lesson_content}

Answer:
{answer}"""

    try:
        response = ollama.chat(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        )
        return response['message']['content']
    except Exception as e:
        logger.error(f"Failed to grade answer: {e}")
        return "Score: 0 | Feedback: Grading service unavailable."