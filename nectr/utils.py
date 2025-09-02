# nectr/utils.py
import yaml
import logging

def load_yaml_config(path: str):
    try:
        with open(path, "r") as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        logging.error(f"Config file not found: {path}")
        return {} # Return empty dict or raise a custom error
    except yaml.YAMLError as e:
        logging.error(f"Error parsing YAML file {path}: {e}")
        return {} # Return empty dict or raise a custom error