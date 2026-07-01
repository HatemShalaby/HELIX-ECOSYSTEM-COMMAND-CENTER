from typing import Union, Dict, List, Any

_quiz_answers = {}

def format_quiz(quiz_data: Union[Dict[str, str], List[str], str]) -> str:
    """
    Standardizes quiz data into Markdown format.
    
    Args:
        quiz_data: Input data (Dict[Question, Answer], List of questions, or raw string)
        
    Returns:
        Formatted Markdown quiz section.
    """
    header = "## Quiz"
    questions_only = []
    answers_only = []
    
    # 1. Handle Empty/None Inputs
    if not quiz_data:
        return f"{header}\n*No quiz content available.*"

    # 2. Handle Dict input (e.g., {'Q1': 'A1'})
    if isinstance(quiz_data, dict):
        topic = str(quiz_data.get("topic", "default")).lower() if "topic" in quiz_data else "default"
        source_data = quiz_data.get("questions", quiz_data)

        if isinstance(source_data, dict):
            questions_only = [str(q) for q in source_data.keys() if q != "topic"]
            answers_only = [str(a) for q, a in source_data.items() if q != "topic"]
        elif isinstance(source_data, list):
            questions_only = [str(q) for q in source_data]

        _quiz_answers[topic] = answers_only
        lines = [f"{i}. {q}" for i, q in enumerate(questions_only, 1)]
        return f"{header}\n" + "\n".join(lines)

    # 3. Handle List input (e.g., ['Q1', 'Q2'])
    if isinstance(quiz_data, list):
        for item in quiz_data:
            item_text = str(item)
            if "Answer:" in item_text:
                question_text, answer_text = item_text.split("Answer:", 1)
                questions_only.append(question_text.strip())
                answers_only.append(answer_text.strip())
            else:
                questions_only.append(item_text)

        _quiz_answers["default"] = answers_only
        lines = [f"{i}. {q}" for i, q in enumerate(questions_only, 1)]
        return f"{header}\n" + "\n".join(lines)

    # 4. Handle String (Already formatted or raw)
    for line in str(quiz_data).splitlines():
        stripped_line = line.strip()
        if not stripped_line:
            continue
        if stripped_line.lower().startswith(("answer:", "correct:")):
            answers_only.append(stripped_line.split(":", 1)[1].strip())
            continue
        if "Answer:" in stripped_line:
            question_text, answer_text = stripped_line.split("Answer:", 1)
            questions_only.append(question_text.strip())
            answers_only.append(answer_text.strip())
            continue
        if "Correct:" in stripped_line:
            question_text, answer_text = stripped_line.split("Correct:", 1)
            questions_only.append(question_text.strip())
            answers_only.append(answer_text.strip())
            continue
        questions_only.append(stripped_line)

    _quiz_answers["default"] = answers_only
    lines = [f"{i}. {q}" for i, q in enumerate(questions_only, 1)]
    return f"{header}\n" + "\n".join(lines)