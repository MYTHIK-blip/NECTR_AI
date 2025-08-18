# run_agent.py
from nectr.agent_core import Agent

if __name__ == "__main__":
    agent = Agent("config/ops_mode.yaml")
    agent.loop()
