import json
from typing import Any, Dict

class ConfigLoader:
    """
    Loads configuration parameters from a JSON file.
    """

    def load_config(self, config_file: str) -> Dict[str, Any]:
        """
        Loads the configuration from a JSON file.

        Args:
            config_file (str): The path to the JSON configuration file.

        Returns:
            Dict[str, Any]: The configuration parameters as a dictionary.
        """
        with open(config_file, 'r') as f:
            return json.load(f)