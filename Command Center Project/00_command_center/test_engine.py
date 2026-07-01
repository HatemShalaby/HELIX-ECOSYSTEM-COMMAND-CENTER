import json
import sys
from pathlib import Path

import pytest

sys.path.append(str(Path(__file__).parent))
from engine import Engine, ResourceGuard, LOG_FILE

@pytest.fixture
def sample_payload():
    return {
        "steps": [
            {"type": "log", "params": {"message": "Starting test"}},
            {"type": "wait", "params": {"duration": 0.1}},
            {"type": "inference", "params": {"prompt": "Test prompt"}},
        ]
    }

def test_engine_execution(sample_payload):
    LOG_FILE.unlink(missing_ok=True)
    # Use a guard that never stalls (threshold 100%)
    guard = ResourceGuard(memory_threshold_percent=100.0)
    engine = Engine(resource_guard=guard)
    engine.execute(sample_payload)
    assert LOG_FILE.exists()
    with open(LOG_FILE) as f:
        log = json.load(f)
    assert len(log) == 3
    assert any("Starting test" in entry["message"] for entry in log)
    assert any("wait" in entry["message"] for entry in log)
    assert any("inference" in entry["message"] for entry in log)

def test_resource_guard_stall(monkeypatch):
    class FakeMem:
        percent = 90.0
    monkeypatch.setattr("psutil.virtual_memory", lambda: FakeMem())
    guard = ResourceGuard()
    assert guard.check_memory() is False  # should stall