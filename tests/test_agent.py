# test_agent.py
import unittest
from nectr.agent_core import Agent

class TestAgentCore(unittest.TestCase):
    def setUp(self):
        self.agent = Agent("config/ops_mode.yaml")

    def test_reason_output(self):
        signal = "Test signal"
        result = self.agent.reason(signal)
        self.assertIn("Test signal", result)

    def test_loop_interval(self):
        interval = self.agent.config["agent"]["loop_interval"]
        self.assertIsInstance(interval, int)

if __name__ == "__main__":
    unittest.main()
