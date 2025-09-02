# nectr/agent_core.py

import time
import logging
from nectr.memory import MemoryManager
from nectr.telemetry import TelemetryLogger
from nectr.utils import load_yaml_config
from nectr.deception_layer import Honeypot
from nectr.swarm_router import SwarmRouter # Added import

class Agent:
    def __init__(self, ops_config_path: str, prompts_config_path: str, identity: str = None): # Added identity parameter
        self.ops_config = load_yaml_config(ops_config_path)
        self.prompts_config = load_yaml_config(prompts_config_path)
        self.memory = MemoryManager(self.ops_config.get("memory"))
        self.logger = TelemetryLogger()
        self.identity = identity if identity else self.ops_config["agent"].get("name", "nectr-alpha") # Use passed identity or default
        self.honeypot = Honeypot(self.logger, name=f"{self.identity}-honeypot")
        self.loop_interval = self.ops_config["agent"].get("loop_interval", 5)
        self.mode = self.ops_config["agent"].get("mode", "default")

        # Ensure the selected mode exists in prompts_config
        if self.mode not in self.prompts_config.get('prompts', {}):
            logging.warning(f"[NECTR] Agent mode '{self.mode}' not found in prompts_config. Falling back to 'default'.")
            self.mode = "default"

        # Access the specific prompt set for the current mode
        current_prompt_set = self.prompts_config['prompts'].get(self.mode, {})

        self.system_prompt = current_prompt_set.get("system", "You are a NECTR AI agent.")
        self.user_template = current_prompt_set.get("user_template", "Observation: {signal}\nRespond accordingly.")

        logging.info(f"[NECTR] Initialized agent '{self.identity}' with interval: {self.loop_interval}s")
        self.router = None # Initialize router to None

    def set_router(self, router: SwarmRouter):
        self.router = router
        self.router.register_agent(self.identity, self)

    def observe(self) -> str:
        """Simulate environmental or sensor input"""
        # Fetch recent memory to simulate remembering past states
        recent_memories = self.memory.fetch_recent(limit=1)
        last_insight = recent_memories[0][2] if recent_memories else "No prior insight."

        # Use the user_template from the loaded prompts_config for the current mode
        # For observe, we'll just return a placeholder for now, but it will be part of the user_template later
        return f"Simulated input signal. Last insight: {last_insight}"

    def reason(self, signal: str) -> str:
        """Simulate cognition or decision-making"""
        # The reasoning step will now incorporate the system prompt and user template
        # This is a simplified representation; a real LLM call would happen here.
        full_prompt = f"{self.system_prompt}\n{self.user_template.format(signal=signal)}"
        return f"Reasoning based on: '{full_prompt}'"

    def act(self, signal: str, insight: str) -> None:
        """Output, communicate, log, or trigger downstream behavior"""
        # The act step will now use the insight derived from reasoning
        print(f"[{self.identity}] Acting on insight: {insight}")
        self.logger.log(f"[{self.identity}] Acting on insight: {insight}")
        self.memory.store(signal, insight) # Store the signal and insight in memory

        # Simulate an attack on the honeypot
        self.honeypot.simulate_attack(attacker_ip="1.2.3.4", attack_type="recon")

        # Send a message to another agent (if router is set)
        if self.router:
            # For simplicity, let's assume another agent with ID 'nectr-beta' exists
            # In a real scenario, agent discovery would be needed.
            target_agent_id = "nectr-beta" if self.identity == "nectr-alpha" else "nectr-alpha"
            message_content = f"Hello from {self.identity}! My insight: {insight[:50]}..."
            self.router.send_message(self.identity, target_agent_id, message_content)

    def receive_message(self, sender_id: str, message: str):
        """Receives a message from another agent."""
        logging.info(f"[NECTR] {self.identity} received message from {sender_id}: {message}")
        self.logger.log(f"[NECTR] {self.identity} received message from {sender_id}: {message}")

    def step(self) -> None:
        """One full cycle of observe → reason → act"""
        signal = self.observe()
        insight = self.reason(signal)
        self.act(signal, insight)

    def loop(self) -> None:
        """Run agent loop indefinitely based on config"""
        while True:
            self.step()
            time.sleep(self.loop_interval)