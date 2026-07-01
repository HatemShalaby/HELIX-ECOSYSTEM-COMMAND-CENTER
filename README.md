# Helix Ecosystem — Command Center Project

## Overview

A production-minded AI automation and learning workspace built for self-directed engineering workflows.

This repository contains a local command engine, a learning system that generates lessons and quizzes, an interactive browser-based quiz experience, and a headless Playwright test harness for automated validation.

## About

This project is designed to demonstrate an engineering-grade local AI platform with explicit operational controls, secure content generation, and human-guided learning workflows.

It is intended for reviewers who want to see:

- a clear separation between automation logic and learning content,
- secure answer handling in browser-based quizzes,
- local model discovery for Ollama-managed models,
- path-centralized configuration, and
- explicit save/discard policies for learner data.

## What’s inside

- `00_command_center/`
  - `engine.py` — JSON-driven command engine with resource-aware execution and structured execution logging.
- `02_learning_system/browser_engine/`
  - `orchestrator.py` — end-to-end learning session coordinator.
  - `education_engine.py` — lesson generation using Ollama-powered local model inference.
  - `quiz_generator.py` — quiz content processor with answers kept server-side.
  - `renderer.py` — Markdown-to-HTML render pipeline with answer leakage protection.
  - `feedback_handler.py` — Flask API that evaluates responses, saves sessions, and discards results on demand.
  - `model_registry.py` — local Ollama model discovery and selection layer.
  - `path_config.py` — single source of truth for repository path constants.
- `06_memory/`
  - persistent learning records, command engine logs, and metacognitive artifacts.
- `Wiki/SYSTEM_ANALYSIS.md`
  - architecture and system design reference.
- `Command Center Project/02_learning_system/PROJECT_STATUS.md`
  - operational status report and active validation state.

## Production-ready value

- Human-in-the-loop learning workflow with explicit save/discard semantics.
- Strong runtime isolation: lesson generation and browser automation run sequentially to avoid shared resource conflicts.
- Answer data is never exposed directly in rendered HTML.
- Local model discovery adapts to available Ollama models and falls back cleanly if none are available.
- Engine-level memory guard protects the host from overload during long-running sessions.

## Quick start

1. Ensure Python 3.11+ is installed.
2. Install Python dependencies:

   ```powershell
   python -m pip install flask flask-cors playwright markdown ollama psutil
   python -m playwright install chromium
   ```

3. Start a local Ollama daemon and confirm it is reachable on `localhost:11434`.
4. Run the learning orchestrator:

   ```powershell
   python "Command Center Project\02_learning_system\browser_engine\orchestrator.py" "Machine Learning"
   ```

5. For an automated validation run:

   ```powershell
   python "Command Center Project\02_learning_system\browser_engine\orchestrator.py" "Machine Learning" --test
   ```

6. Review saved session records in `Command Center Project\02_learning_system\learning-records/` and logs in `Command Center Project\06_memory/`.

## Command Center Engine usage

The command engine is designed for scripted payload execution:

```python
from Command_Center_Project.00_command_center.engine import Engine
payload = {
    "steps": [
        {"type": "log", "params": {"message": "Start session"}},
        {"type": "wait", "params": {"duration": 1}},
        {"type": "inference", "params": {"prompt": "Summarize key risks."}}
    ]
}
Engine().execute(payload)
```

## Current status

The repository is actively maintained and organized as a working AI automation environment. Core systems are implemented, and the project is positioned for further engineering polish, integration with CI/CD, and model registry hardening.

## License

This project is licensed under the terms described in `LICENSE`.
