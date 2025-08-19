# nectr/agent_core.py

import time
import logging
from nectr.memory import MemoryManager
from nectr.telemetry import TelemetryLogger
from nectr.utils import load_yaml_config


class Agent:
    def __init__(self, config_path: str):
        self.config = load_yaml_config(config_path)
        self.memory = MemoryManager(self.config.get("memory"))
        self.logger = TelemetryLogger()
        self.identity = self.config["agent"].get("name", "nectr-alpha")
        self.loop_interval = self.config["agent"].get("loop_interval", 5)

        logging.info(f"[NECTR] Initialized agent '{self.identity}' with interval: {self.loop_interval}s")

    def observe(self) -> str:
        """Simulate environmental or sensor input"""
        return "Simulated input signal."

    def reason(self, signal: str) -> str:
        """Simulate cognition or decision-making"""
        return f"Refined insight based on '{signal}'"

    def act(self, insight: str) -> None:
        """Output, communicate, log, or trigger downstream behavior"""
        print(f"[{self.identity}] Responding with: {insight}")
        self.logger.log(insight)

    def step(self) -> None:
        """One full cycle of observe → reason → act"""
        signal = self.observe()
        insight = self.reason(signal)
        self.act(insight)

    def loop(self) -> None:
        """Run agent loop indefinitely based on config"""
        while True:
            self.step()
            time.sleep(self.loop_interval)
