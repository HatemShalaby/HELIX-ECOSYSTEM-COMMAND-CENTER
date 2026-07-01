import json
import time
import sys
from pathlib import Path
from typing import Any
import logging

logger = logging.getLogger("engine")

# ---- Dynamic model lookup (temporary, until model_registry is updated) ----
def get_model(role: str = "default_lesson_model") -> str:
    """Return the best available local model for the given role.
    This can later be replaced by model_registry.get_model(role).
    """
    try:
        import ollama
        models = ollama.list()
        # Prefer lfm2.5:8b as it fits GPU and is fast; fallback to first model
        preferred = "lfm2.5:8b"
        available = [m.model for m in models]
        if preferred in available:
            return preferred
        # Fallbacks
        for fallback in ["qwen3:8b", "deepseek-r1:latest"]:
            if fallback in available:
                return fallback
        if available:
            return available[0]
        return "lfm2.5:8b"  # ultimate fallback
    except Exception:
        return "lfm2.5:8b"
# ----------------------------------------------------------------

LOG_FILE = Path(r"H:\AI Automation Engineering\Command Center Project\06_memory\command_center_log.json")


class ResourceGuard:
    def __init__(self, memory_threshold_percent: float = 80.0):
        self.threshold = memory_threshold_percent
        try:
            import psutil
            self._psutil = psutil
        except ImportError:
            raise ImportError("psutil is required. Install with: pip install psutil")

    def check_memory(self) -> bool:
        mem = self._psutil.virtual_memory()
        if mem.percent < self.threshold:
            return True
        print(f"Memory usage {mem.percent:.1f}% exceeds threshold {self.threshold}%, stalling...")
        time.sleep(5)
        return False

class Engine:
    def __init__(self, resource_guard: ResourceGuard | None = None):
        self.guard = resource_guard or ResourceGuard()
        self.log_entries = []

    def execute(self, payload: dict[str, Any]) -> None:
        steps = payload.get("steps", [])
        model_name = get_model("default_lesson_model")  # dynamic, no hardcoded model
        print(f"Engine initialized. Using model: {model_name}")

        for i, step in enumerate(steps, 1):
            if not self.guard.check_memory():
                self.log(f"Step {i}: stalled due to memory")
                continue

            step_type = step.get("type")
            params = step.get("params", {})
            if step_type == "log":
                msg = params.get("message", "")
                print(msg)
                self.log(f"Step {i}: log - {msg}")
            elif step_type == "wait":
                duration = params.get("duration", 1)
                time.sleep(duration)
                self.log(f"Step {i}: wait - {duration}s")
            elif step_type == "inference":
                prompt = params.get("prompt", "")
                print(f"Would call model {model_name} with: {prompt[:50]}...")
                self.log(f"Step {i}: inference prompt logged")
            else:
                self.log(f"Step {i}: unknown type {step_type}")

        self.save_log()

    def log(self, message: str) -> None:
        self.log_entries.append({"timestamp": time.time(), "message": message})

    def save_log(self) -> None:
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            json.dump(self.log_entries, f, indent=2)