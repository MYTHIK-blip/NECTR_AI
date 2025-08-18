# nectr/optimizer.py

import yaml
import json
from nectr.memory import load_memory
from nectr.telemetry import load_telemetry

class Optimizer:
    def __init__(self, rule_path="config/optimization_rules.yaml", config_path="config/ops_mode.yaml"):
        self.rules = self.load_yaml(rule_path)
        self.config_path = config_path
        self.current_config = self.load_yaml(config_path)
        self.changes = []

    def load_yaml(self, path):
        with open(path, "r") as f:
            return yaml.safe_load(f)

    def score_conditions(self, memory, telemetry):
        # Passive example: if > N passive loops with no new info, decrease loop_interval
        loop_count = len(memory)
        if loop_count > self.rules['loop_interval']['threshold']:
            self.changes.append({
                "field": "agent.loop_interval",
                "from": self.current_config["agent"]["loop_interval"],
                "to": max(1, self.current_config["agent"]["loop_interval"] - 1),
                "reason": "High loop count without semantic change"
            })

    def apply_changes(self):
        for change in self.changes:
            parts = change['field'].split(".")
            ref = self.current_config
            for p in parts[:-1]:
                ref = ref[p]
            ref[parts[-1]] = change['to']
        with open(self.config_path, "w") as f:
            yaml.dump(self.current_config, f)

    def run(self):
        memory = load_memory(limit=50)
        telemetry = load_telemetry(limit=50)
        self.score_conditions(memory, telemetry)
        if self.changes:
            self.apply_changes()
            print(f"[OPTIMIZER] Changes applied: {self.changes}")
        else:
            print("[OPTIMIZER] No changes needed.")

if __name__ == "__main__":
    Optimizer().run()
