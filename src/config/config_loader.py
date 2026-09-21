import os
import yaml
from typing import Dict, Any

class ConfigLoader:
    """Loads and provides access to YAML configuration files."""
    _instance = None
    _config: Dict[str, Any] = {}
    _thresholds: Dict[str, Any] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigLoader, cls).__new__(cls)
            cls._instance._load_configs()
        return cls._instance

    def _load_configs(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        
        settings_path = os.path.join(base_dir, 'config', 'settings.yaml')
        if os.path.exists(settings_path):
            with open(settings_path, 'r') as f:
                self._config = yaml.safe_load(f) or {}

        thresholds_path = os.path.join(base_dir, 'config', 'thresholds.yaml')
        if os.path.exists(thresholds_path):
            with open(thresholds_path, 'r') as f:
                self._thresholds = yaml.safe_load(f) or {}

    def get(self, key: str, default: Any = None) -> Any:
        """Get a value from settings.yaml using dot notation (e.g., 'app.name')."""
        keys = key.split('.')
        val = self._config
        try:
            for k in keys:
                val = val[k]
            return val
        except (KeyError, TypeError):
            return default

    def get_threshold(self, key: str, default: Any = None) -> Any:
        """Get a value from thresholds.yaml using dot notation."""
        keys = key.split('.')
        val = self._thresholds
        try:
            for k in keys:
                val = val[k]
            return val
        except (KeyError, TypeError):
            return default
