# nectr/optimizer.py

import yaml
import json
import logging
from nectr.memory import MemoryManager
from nectr.telemetry import TelemetryLogger


class Optimizer:
    def __init__(self, rule_path="config/optimization_rules.yaml", config_path="config/ops_mode.yaml"):
        self.rule_path = rule_path
        self.config_path = config_path
        self.rules = self._load_yaml(self.rule_path)
        self.current_config = self._load_yaml(self.config_path)
        self.changes = []
        self.memory_manager = MemoryManager(self.current_config.get("memory", {}))
        self.telemetry_logger = TelemetryLogger(self.current_config.get("telemetry", {}).get("log_path"))

    def _load_yaml(self, path):
        try:
            with open(path, "r") as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            logging.error(f"Config file not found: {path}")
            return {}
        except yaml.YAMLError as e:
            logging.error(f"Error parsing YAML file {path}: {e}")
            return {}

    def score_conditions(self, memory, telemetry):
        # Passive example: if > N passive loops with no new info, decrease loop_interval
        loop_count = len(memory)
        if 'loop_interval' in self.rules and 'threshold' in self.rules['loop_interval']:
            if loop_count > self.rules['loop_interval']['threshold']:
                self.changes.append({
                    "field": "agent.loop_interval",
                    "from": self.current_config["agent"]["loop_interval"],
                    "to": max(1, self.current_config["agent"]["loop_interval"] - 1),
                    "reason": "High loop count without semantic change"
                })

    def apply_changes(self):
        try:
            for change in self.changes:
                parts = change['field'].split(".")
                ref = self.current_config
                for p in parts[:-1]:
                    ref = ref[p]
                ref[parts[-1]] = change['to']
            with open(self.config_path, "w") as f:
                yaml.dump(self.current_config, f)
        except (IOError, yaml.YAMLError) as e:
            logging.error(f"Error applying changes to config file {self.config_path}: {e}")

    def run(self):
        memory = self.memory_manager.fetch_recent(limit=50)
        telemetry = self.telemetry_logger.get_recent_logs(limit=50)
        self.score_conditions(memory, telemetry)
        if self.changes:
            self.apply_changes()
            logging.info(f"[OPTIMIZER] Changes applied: {self.changes}")
        else:
            logging.info("[OPTIMIZER] No changes needed.")

if __name__ == "__main__":
    # Create dummy config files for standalone run
    import os
    if not os.path.exists("config/optimization_rules.yaml"):
        os.makedirs("config", exist_ok=True)
        with open("config/optimization_rules.yaml", "w") as f:
            f.write("loop_interval:\n  threshold: 5\n")
    if not os.path.exists("config/ops_mode.yaml"):
        with open("config/ops_mode.yaml", "w") as f:
            f.write("agent:\n  name: \"test-optimizer-agent\"\n  loop_interval: 10\nmemory:\n  path: \"data/memory.sqlite\"\ntelemetry:\n  log_path: \"data/attack_logs/agent.log\"\n")

    Optimizer().run()