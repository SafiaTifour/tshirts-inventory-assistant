import yaml
import os
from typing import Dict, Any

def load_settings() -> Dict[str, Any]:
    """
    Load settings from config.yaml file
    
    Returns:
        Dict: Dictionary containing all configuration settings
    """
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config/config.yaml')
    
    try:
        with open(config_path, 'r') as config_file:
            settings = yaml.safe_load(config_file)
        return settings
    except Exception as e:
        raise Exception(f"Failed to load configuration: {str(e)}")