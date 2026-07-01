import sys
import os
import json
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("model_registry")

# Path to local registry config
CONFIG_PATH = Path(__file__).parent / "model_config.json"

DEFAULT_PREFERENCES = {
    "default_lesson_model": [],
    "default_quiz_model": [],
    "default_grading_model": []
}

def load_config() -> dict:
    """Loads configuration from JSON file or returns defaults."""
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Failed to read model_config.json: {e}. Using defaults.")
    return DEFAULT_PREFERENCES

def save_config(config: dict):
    """Saves configuration to JSON file."""
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4)
    except Exception as e:
        logger.error(f"Failed to write model_config.json: {e}")

def get_available_local_models() -> list:
    """Pings the local Ollama daemon to get a list of installed models."""
    try:
        import ollama
        models_response = ollama.list()
        # Parse list of models
        available = []
        if hasattr(models_response, 'models'):
            available = [m.model for m in models_response.models]
        elif isinstance(models_response, dict) and 'models' in models_response:
            available = [m.get('model') if isinstance(m, dict) else getattr(m, 'model', str(m)) for m in models_response['models']]
        elif isinstance(models_response, list):
            available = [getattr(m, 'model', str(m)) for m in models_response]
        
        # Clean model names (e.g. remove trailing tags if necessary, but keep exact tag for matching)
        return [m.strip() for m in available if m]
    except Exception as e:
        logger.warning(f"Ollama daemon query failed or offline: {e}")
        return []

def get_model(role: str) -> str:
    """
    Selects the most appropriate available model for a given role based on preferences.
    Fails gracefully if no models are available.
    """
    config = load_config()
    preferences = config.get(role, DEFAULT_PREFERENCES.get(role, []))
    
    available_models = get_available_local_models()
    
    if not available_models:
        logger.warning("No local models found on the Ollama daemon. Falling back to stub mode.")
        return "stub-model"
    
    # 1. Look for the first preference that is available
    for pref in preferences:
        if pref in available_models:
            return pref
        # Try finding a partial match
        for available in available_models:
            if pref.split(':')[0] == available.split(':')[0]:
                return available
                
    # 2. Fall back to any available model
    fallback = available_models[0]
    logger.info(f"Preferred model for '{role}' not found. Falling back to available model: '{fallback}'")
    return fallback

if __name__ == "__main__":
    # Self-test/registration info
    print("--- Model Registry Audit ---")
    available = get_available_local_models()
    print(f"Available local models: {available}")
    for role in DEFAULT_PREFERENCES.keys():
        print(f"Active model for '{role}': {get_model(role)}")