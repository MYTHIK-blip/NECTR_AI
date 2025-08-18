# tests/test_optimizer.py

import unittest
from nectr.optimizer import Optimizer

class TestOptimizer(unittest.TestCase):
    def test_optimizer_runs_without_crashing(self):
        opt = Optimizer()
        try:
            opt.run()
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"Optimizer crashed: {e}")

if __name__ == "__main__":
    unittest.main()
