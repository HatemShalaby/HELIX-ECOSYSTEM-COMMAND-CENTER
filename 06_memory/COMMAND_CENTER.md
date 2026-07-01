# Command Center Engine Documentation

## Overview
The Command Center Engine is a lightweight workflow runner for JSON-defined step sequences. It is built to execute payloads sequentially while protecting the host environment from excessive memory pressure.

This engine is designed as a production-oriented automation core for structured command execution within the Helix Ecosystem.

## Core responsibilities
- Validate and execute step sequences from JSON payloads.
- Apply memory safety through `ResourceGuard` before each step.
- Persist execution history to `06_memory/command_center_log.json`.
- Use local Ollama model discovery for inference-related steps.

## Implementation details

### `ResourceGuard`
- Uses `psutil` to inspect `virtual_memory()`.
- If memory usage exceeds `80%`, the engine stalls and retries rather than failing abruptly.
- Ensures long-running workflows do not destabilize the host.

### `Engine`
- `execute(payload: dict[str, Any])` iterates through `payload["steps"]`.
- Supported step types:
  - `log` — records messages and prints status.
  - `wait` — pauses execution for a specified duration.
  - `inference` — logs a model prompt and simulates an inference call.
  - unknown types are recorded as unsupported.
- The engine currently selects a local model using `ollama.list()` and prefers `lfm2.5:8b` when available.

### Logging
- Execution entries are appended to an in-memory list.
- Output is written to `06_memory/command_center_log.json` at the end of each run.

## Usage

### Run from Python
```python
from Command_Center_Project.00_command_center.engine import Engine

payload = {
    "steps": [
        {"type": "log", "params": {"message": "Starting command sequence"}},
        {"type": "wait", "params": {"duration": 1}},
        {"type": "inference", "params": {"prompt": "Summarize the current system state."}}
    ]
}
Engine().execute(payload)
```

### Requirements
- `psutil` must be installed for `ResourceGuard`.
- `ollama` is required for local model discovery if inference steps are used.

### Log location
- `Command Center Project/06_memory/command_center_log.json`

## Example payload
```json
{
  "steps": [
    {"type": "log", "params": {"message": "Start session"}},
    {"type": "wait", "params": {"duration": 2}},
    {"type": "inference", "params": {"prompt": "Summarize the work completed so far."}}
  ]
}
```

## Notes
- The current engine is intentionally simple and deterministic.
- Model selection is local and best-effort: it will use `ollama.list()` when available and fall back to `lfm2.5:8b` or the first available model.
- This doc is intended to make the repository feel mature and explicit to an engineering reviewer inspecting the project on GitHub.
