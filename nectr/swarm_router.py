# nectr/swarm_router.py

import logging

class SwarmRouter:
    def __init__(self):
        self.registered_agents = {}
        logging.info("[SWARM] SwarmRouter initialized.")

    def register_agent(self, agent_id: str, agent_instance):
        """Registers an agent with the router."""
        if agent_id in self.registered_agents:
            logging.warning(f"[SWARM] Agent ID '{agent_id}' already registered. Overwriting.")
        self.registered_agents[agent_id] = agent_instance
        logging.info(f"[SWARM] Agent '{agent_id}' registered with SwarmRouter.")

    def send_message(self, sender_id: str, receiver_id: str, message: str):
        """Sends a message from one agent to another."""
        if receiver_id not in self.registered_agents:
            logging.error(f"[SWARM] Receiver agent '{receiver_id}' not found.")
            return False

        receiver_agent = self.registered_agents[receiver_id]
        logging.info(f"[SWARM] Message from '{sender_id}' to '{receiver_id}': {message}")
        receiver_agent.receive_message(sender_id, message)
        return True

    def broadcast_message(self, sender_id: str, message: str):
        """Broadcasts a message to all registered agents except the sender."""
        for agent_id, agent_instance in self.registered_agents.items():
            if agent_id != sender_id:
                self.send_message(sender_id, agent_id, message)