import unittest
from unittest.mock import MagicMock, patch
from nectr.agent_core import Agent
from nectr.telemetry import TelemetryLogger
from nectr.memory import MemoryManager
from nectr.swarm_router import SwarmRouter
from nectr.deception_layer import Honeypot
import os

class TestAgentCore(unittest.TestCase):
    def setUp(self):
        # Create dummy config files for testing
        self.ops_config_path = "config/test_ops_mode.yaml"
        self.prompts_config_path = "config/test_prompts.yaml"
        self.memory_db_path = "data/test_memory.sqlite"

        os.makedirs("config", exist_ok=True)
        os.makedirs("data", exist_ok=True)

        with open(self.ops_config_path, "w") as f:
            f.write("""
agent:
  name: "test-agent"
  loop_interval: 1
  mode: "default"
memory:
  path: "data/test_memory.sqlite"
""")
        with open(self.prompts_config_path, "w") as f:
            f.write("""
prompts:
  default:
    system: "You are a test agent."
    user_template: "Input: {signal}"
""")
        # Initialize Agent with test configs
        self.agent = Agent(self.ops_config_path, self.prompts_config_path, identity="test-agent-alpha")

    def tearDown(self):
        # Clean up dummy config files and memory DB
        os.remove(self.ops_config_path)
        os.remove(self.prompts_config_path)
        if os.path.exists(self.memory_db_path):
            os.remove(self.memory_db_path)

    def test_agent_initialization(self):
        self.assertIsInstance(self.agent.logger, TelemetryLogger)
        self.assertIsInstance(self.agent.memory, MemoryManager)
        self.assertIsInstance(self.agent.honeypot, Honeypot)
        self.assertEqual(self.agent.identity, "test-agent-alpha")
        self.assertEqual(self.agent.loop_interval, 1)
        self.assertEqual(self.agent.mode, "default")
        self.assertEqual(self.agent.system_prompt, "You are a test agent.")

    @patch('nectr.telemetry.TelemetryLogger.log')
    def test_act_method(self, mock_log):
        signal = "test_signal"
        insight = "test_insight"
        self.agent.act(signal, insight)
        mock_log.assert_called() # Ensure logging happened
        # Verify memory store (indirectly, by checking if no error)

    @patch('nectr.telemetry.TelemetryLogger.log')
    def test_receive_message(self, mock_log):
        sender = "other-agent"
        message = "Hello from other agent!"
        self.agent.receive_message(sender, message)
        mock_log.assert_called_with(f"[NECTR] test-agent-alpha received message from {sender}: {message}")

    def test_memory_persistence(self):
        # Store an insight
        signal = "initial_signal"
        insight = "initial_insight"
        self.agent.act(signal, insight)

        # Create a new agent instance to simulate persistence
        new_agent = Agent(self.ops_config_path, self.prompts_config_path, identity="test-agent-beta")
        
        # Observe with the new agent, should retrieve the last insight
        observed_signal = new_agent.observe()
        self.assertIn(insight, observed_signal)

if __name__ == "__main__":
    unittest.main()