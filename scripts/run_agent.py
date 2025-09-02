# scripts/run_agent.py

import argparse
import logging
import sys
from nectr.agent_core import Agent
from nectr.swarm_router import SwarmRouter # Added import

def parse_args():
    parser = argparse.ArgumentParser(description="Run the NECTR agent.")
    parser.add_argument(
        "--ops-config", type=str, default="config/ops_mode.yaml",
        help="Path to the agent's operational mode config YAML file"
    )
    parser.add_argument(
        "--prompts-config", type=str, default="config/prompts.yaml",
        help="Path to the agent's prompts config YAML file"
    )
    parser.add_argument(
        "--once", action="store_true",
        help="Run the agent loop once and exit (for debugging/testing)"
    )
    return parser.parse_args()

def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)]
    )

def main():
    args = parse_args()
    configure_logging()

    logging.info("[NECTR] Booting agent with ops config: %s and prompts config: %s", args.ops_config, args.prompts_config)

    # Initialize SwarmRouter
    router = SwarmRouter()

    # Initialize two agents
    agent_alpha = Agent(args.ops_config, args.prompts_config, identity="nectr-alpha")
    agent_alpha.set_router(router)

    agent_beta = Agent(args.ops_config, args.prompts_config, identity="nectr-beta")
    agent_beta.set_router(router)

    # For --once, run one step for each agent
    if args.once:
        logging.info("[NECTR] Running agent_alpha step...")
        agent_alpha.step()

        # Simulate a simple adversarial action
        logging.info("[NECTR] Simulating adversarial action...")
        adversary_action = "Malicious packet detected from 5.6.7.8"
        agent_alpha.receive_message("adversary", adversary_action) # Agent alpha detects the adversary

        logging.info("[NECTR] Running agent_beta step...")
        agent_beta.step()

    else:
        # For continuous loop, we'll need a more sophisticated scheduler
        logging.warning("[NECTR] Continuous loop for multiple agents not yet implemented. Running --once mode.")
        agent_alpha.step()
        agent_beta.step()

if __name__ == "__main__":
    main()
