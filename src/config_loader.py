import json

class ConfigLoader:
    """
    Loads configuration parameters from a JSON file.
    """
    def load_config(self, config_file):
        with open(config_file, 'r') as f:
            return json.load(f)