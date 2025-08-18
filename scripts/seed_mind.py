# seed_mind.py
from nectr.memory import MemoryManager

seed_data = [
    ("Observe anomaly at honeypot entry", "Deploy decoy expansion swarm."),
    ("Detected repeat pattern", "Enable symbolic reroute."),
    ("FRI spike", "Throttle feedback logging.")
]

def seed():
    mm = MemoryManager({"path": "data/memory.sqlite"})
    for signal, insight in seed_data:
        mm.store(signal, insight)
    print("🧠 Memory seeded.")

if __name__ == "__main__":
    seed()
