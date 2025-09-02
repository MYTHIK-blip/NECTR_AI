import unittest
from unittest.mock import MagicMock, patch
from nectr.optimizer import Optimizer
import os

class TestOptimizer(unittest.TestCase):
    def setUp(self):
        # Create dummy config files for testing
        self.rule_path = "config/test_optimization_rules.yaml"
        self.config_path = "config/test_ops_mode.yaml"
        self.log_path = "data/test_optimizer.log" # For TelemetryLogger

        os.makedirs("config", exist_ok=True)
        os.makedirs("data", exist_ok=True)

        with open(self.rule_path, "w") as f:
            f.write("""
loop_interval:
  threshold: 5
""")
        with open(self.config_path, "w") as f:
            f.write("""
agent:
  name: "test-optimizer-agent"
  loop_interval: 10
memory:
  path: "data/test_memory.sqlite"
telemetry:
  log_path: "data/test_optimizer.log"
""")
        # Initialize Optimizer with test configs
        self.optimizer = Optimizer(self.rule_path, self.config_path)

    def tearDown(self):
        # Clean up dummy config files and log file
        os.remove(self.rule_path)
        os.remove(self.config_path)
        if os.path.exists(self.log_path):
            os.remove(self.log_path)
        if os.path.exists("data/test_memory.sqlite"):
            os.remove("data/test_memory.sqlite")

    @patch('nectr.memory.MemoryManager.fetch_recent')
    @patch('nectr.telemetry.TelemetryLogger.get_recent_logs')
    @patch('nectr.optimizer.Optimizer._load_yaml') # Patch _load_yaml to control config loading
    def test_optimizer_run_no_changes(self, mock_load_yaml, mock_get_recent_logs, mock_fetch_recent):
        # Mock _load_yaml to return controlled configs
        mock_load_yaml.side_effect = [
            {'loop_interval': {'threshold': 5}}, # rules
            {'agent': {'name': 'test-optimizer-agent', 'loop_interval': 10}, 'memory': {'path': 'data/test_memory.sqlite'}, 'telemetry': {'log_path': 'data/test_optimizer.log'}} # current_config
        ]

        mock_fetch_recent.return_value = [("ts", "sig", "insight")] * 3 # Less than threshold
        mock_get_recent_logs.return_value = ["log1", "log2", "log3"]

        optimizer = Optimizer(self.rule_path, self.config_path) # Re-initialize with mocks
        optimizer.run()
        self.assertEqual(optimizer.changes, []) # No changes expected

    @patch('nectr.memory.MemoryManager.fetch_recent')
    @patch('nectr.telemetry.TelemetryLogger.get_recent_logs')
    @patch('nectr.optimizer.Optimizer._load_yaml') # Patch _load_yaml to control config loading
    def test_optimizer_run_with_changes(self, mock_load_yaml, mock_get_recent_logs, mock_fetch_recent):
        # Mock _load_yaml to return controlled configs
        mock_load_yaml.side_effect = [
            {'loop_interval': {'threshold': 3}}, # rules
            {'agent': {'name': 'test-optimizer-agent', 'loop_interval': 10}, 'memory': {'path': 'data/test_memory.sqlite'}, 'telemetry': {'log_path': 'data/test_optimizer.log'}} # current_config
        ]

        mock_fetch_recent.return_value = [("ts", "sig", "insight")] * 5 # More than threshold
        mock_get_recent_logs.return_value = ["log1", "log2", "log3", "log4", "log5"]

        optimizer = Optimizer(self.rule_path, self.config_path) # Re-initialize with mocks
        optimizer.run()
        self.assertGreater(len(optimizer.changes), 0) # Expect changes
        self.assertEqual(optimizer.changes[0]['field'], "agent.loop_interval")
        self.assertEqual(optimizer.changes[0]['to'], 9) # 10 - 1

if __name__ == "__main__":
    unittest.main()