# Command Center Engine Documentation

## Overview
The Command Center Engine is designed to process JSON payloads, dynamically import models, and log execution details. It includes a memory guard to ensure sufficient resources are available.

### Key Features:
- **Dynamic Model Loading**: Loads models based on payload specifications.
- **Execution Logging**: Records start time, end time, and duration of each command.
- **Memory Guard**: Monitors memory usage before processing payloads.
- **JSON Payload Processing**: Parses and executes commands step-by-step from JSON payloads.

## Implementation Details
### Engine Class
- **Attributes**:
  - `payload`: Stores the input JSON payload.
- **Methods**:
  - `process_payload()`: Processes each command step in the payload, dynamically loading required models using `model_registry`.
  - `run()`: Initiates the processing of a payload and logs execution duration.
  - `log_result()`: Logs the result of the command execution to a JSON file.

### ResourceGuard Class
- **Static Method**:
  - `check_memory()`: Checks available memory and raises an exception if below a threshold (500 MB in this case).

## Usage Instructions
1. Ensure `model_registry.py` is correctly implemented for dynamic model loading.
2. Place the payload JSON files in the appropriate directory as specified.
3. Run tests using:
   ```
   python -m pytest test_engine.py -v
   ```
4. Check `command_center_log.json` for execution logs.

## Example Payload Structure
```json
{
  "steps": [
    {
      "type": "load_model",
      "model_name": "image_recognition"
    },
    {
      "type": "execute_command",
      "command": "analyze_images"
    }
  ]
}