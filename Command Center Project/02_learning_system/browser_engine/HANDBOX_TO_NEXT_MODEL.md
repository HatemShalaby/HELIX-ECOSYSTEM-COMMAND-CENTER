# HANDOFF TO NEXT MODEL
**Date:** 2026-06-26  
**System:** Helix Ecosystem — Learning System + Command Center Engine  
**State at handoff:** All 8 code fixes complete. System clean and human-in-loop compliant.

---

## What This System Does

An automated self-study engine that:
1. Generates structured lessons on any topic using a local LLM via Ollama
2. Builds quizzes with questions separated from answers (answers never leave the server)
3. Grades student responses in real-time using a strict rubric
4. Holds all session data in RAM until the human explicitly saves or discards
5. Writes session records and updates a metacognitive performance log only on human confirmation

---

## File Map — What Each File Does

| File | Role |
|------|------|
| `path_config.py` | **Start here.** Single source of truth for all project paths. Import from this, never construct raw paths. |
| `model_registry.py` | Dynamic model selection. Calls Ollama at runtime. `get_model(role)` is the only interface. |
| `education_engine.py` | Two functions: `create_lesson(topic)` generates lesson markdown; `grade_answer(answer, lesson_content)` grades with strict rubric. |
| `quiz_generator.py` | `format_quiz(quiz_data)` strips answers, returns question-only markdown. Answers stored in `_quiz_answers` dict in RAM. |
| `quiz_automator.py` | Calls LLM to generate quiz questions for lesson files. Appends to markdown via `format_quiz`. |
| `renderer.py` | Converts lesson markdown to interactive HTML. Strips any answer text before rendering. JS fetches questions from API — never from page source. |
| `feedback_handler.py` | Flask server on port 5000. `/submit` grades and holds in RAM. `/save_session` writes to disk. `/discard_session` clears RAM. `/api/questions` returns question text only. |
| `orchestrator.py` | Top-level coordinator. Human mode: generates lesson → serves URL → waits for browser session. Auto-test mode: headless Playwright + auto-save on completion. |
| `engine.py` | Command Center: processes JSON payloads step-by-step. Memory-guarded. Logs to `command_center_log.json`. |
| `test_integration.py` | Playwright browser connectivity test. Writes result to `RECORDS_DIR`. |

---

## How to Run

### Human Study Mode
```bash
cd browser_engine
.venv\Scripts\activate
python orchestrator.py "Your Topic Here"
```
- Opens a browser URL for the quiz
- Human completes quiz in browser
- Click **Save** to write session to disk, **Discard** to clear, **Retake** to restart

### Automated Test Mode
```bash
python orchestrator.py "Your Topic Here" --test
```
- Headless Playwright submits mock answers
- Auto-calls `/save_session` on completion
- Writes to `learning-records/`

### Command Center Engine
```bash
python engine.py
# or test:
python -m pytest test_engine.py -v
```

---

## Critical Architecture Rules

These are non-negotiable. Breaking any of them corrupts the system:

**1. Path management**  
All paths come from `path_config.py`. Never construct a raw `H:\AI...` string.  
`from path_config import LESSONS_DIR, RECORDS_DIR, MEMORY_DIR, TRACKER_PATH`

**2. Model selection**  
Always use `get_model(role)` from `model_registry`. Never name a model directly in source.  
Valid roles: `"default_lesson_model"`, `"default_quiz_model"`, `"default_grading_model"`

**3. Disk writes**  
Only `/save_session` writes to disk. Only triggered by human action or auto-test completion.  
`/submit` grades in RAM only. Nothing touches disk mid-quiz.

**4. Answer security**  
Answers are stored in `_quiz_answers` dict in `quiz_generator.py` (RAM only).  
The HTML page fetches questions from `/api/questions`. The correct answers are never sent to the client.

**5. Sequential execution**  
LLM inference (Ollama) and Playwright browser never run simultaneously.  
`orchestrator.py` ensures lesson generation completes before the browser launches.

---

## Dynamic Model Discovery

`model_registry.py` queries `ollama.list()` at runtime. It reads role preferences from `model_config.json` (create this file to override defaults). If no config exists or no preferred model is available, it falls back to the first model Ollama reports.

To set preferred models without touching source code, create `browser_engine/model_config.json`:
```json
{
    "default_lesson_model": ["gemma16k", "qwen3:8b"],
    "default_quiz_model": ["lfm2.5:8b", "qwen3:8b"],
    "default_grading_model": ["lfm2.5:8b", "qwen3:8b"]
}
```

---

## Save / Discard Flow

```
Human answers quiz question
        ↓
POST /submit → grade_answer() called → result held in session_answers[] (RAM)
        ↓
Human clicks Save
        ↓
POST /save_session
    → writes session_{topic}_{timestamp}.md to RECORDS_DIR
    → appends to TRACKER_PATH
    → appends entry to metacognitive_log.json
    → clears session_answers[]
        ↓
OR Human clicks Discard
        ↓
POST /discard_session → clears session_answers[] → nothing written
```

---

## What Needs to Happen Next

| Priority | Task |
|----------|------|
| 🔴 P0 | Create `model_config.json` with your preferred models per role |
| 🔴 P0 | Run end-to-end live test: `python orchestrator.py "Python Basics"` in human mode |
| 🟡 P1 | Wire metacognitive log reads back into orchestrator for adaptive quiz difficulty |
| 🟡 P1 | Add Save/Discard/Retake buttons to the rendered HTML (currently API endpoints exist, UI buttons not yet wired) |
| 🟢 P2 | Begin Helix OPS intake pipeline (next major module) |

---

## What Was Broken at Last Handoff (Now Fixed)

- `grade_answer()` did not exist — fatal crash on every quiz submission → **Fixed**
- `model_registry.py` had two competing `get_model()` functions, one with hardcoded `"lfm2.5:8b"` → **Fixed**
- `path_config.py` did not exist — 8 files had raw absolute paths → **Fixed**
- Session records written automatically without human consent → **Fixed**
- Quiz answers embedded in rendered HTML (answer leakage) → **Fixed**
- Grading LLM awarded 20–70 points to nonsense placeholder responses → **Fixed** (strict rubric enforced)