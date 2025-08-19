# scripts/run_agent.py

import argparse
import logging
import sys
from nectr.agent_core import Agent

def parse_args():
    parser = argparse.ArgumentParser(description="Run the NECTR agent.")
    parser.add_argument(
        "--config", type=str, default="config/ops_mode.yaml",
        help="Path to the agent's config YAML file"
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

    logging.info("[NECTR] Booting agent with config: %s", args.config)
    agent = Agent(args.config)

    try:
        if args.once:
            agent.step()  # Run one loop iteration
        else:
            agent.loop()  # Continuous loop
    except KeyboardInterrupt:
        logging.info("[NECTR] Shutdown requested via Ctrl+C")
    except Exception as e:
        logging.error("[NECTR] Unhandled exception: %s", e)
        raise

if __name__ == "__main__":
    main()
