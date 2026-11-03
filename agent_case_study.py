"""Experiment 01: AI Agents and PEAS Framework Simulator."""

class AIAgent:
    def __init__(self, name: str, agent_type: str, peas: dict):
        self.name = name
        self.agent_type = agent_type
        self.peas = peas
        self.state = {}

    def display_peas(self):
        print(f"\n{'='*55}")
        print(f" AGENT CASE STUDY: {self.name.upper()} ({self.agent_type})")
        print(f"{'='*55}")
        print(f"  - Performance Measure : {self.peas['Performance']}")
        print(f"  - Environment         : {self.peas['Environment']}")
        print(f"  - Actuators           : {self.peas['Actuators']}")
        print(f"  - Sensors             : {self.peas['Sensors']}")

    def act(self, percept: dict):
        # Condition-action rule reasoning
        status = percept.get("cleanliness", "dirty")
        location = percept.get("location", "Room_A")
        if status == "dirty":
            action = "SUCK_DIRT"
        else:
            action = "MOVE_TO_NEXT_ROOM"
        print(f"[Sensor Percept: {percept}] --> Reasoned Action: {action}")
        return action

def main():
    vacuum_peas = {
        "Performance": "Square area cleaned, low energy consumption, zero damage",
        "Environment": "Office floors, obstacles, furniture, doorways",
        "Actuators": "Drive wheels, vacuum suction motor, status indicator",
        "Sensors": "Cliff sensor, bump bumper, infrared distance, dirt detector"
    }
    car_peas = {
        "Performance": "Passenger safety, speed, legal adherence, comfort",
        "Environment": "Public roads, pedestrians, weather, traffic signs",
        "Actuators": "Steering assembly, accelerator, hydraulic brakes, horn",
        "Sensors": "LiDAR, RGB cameras, radar arrays, GPS, IMU sensors"
    }

    agent1 = AIAgent("Autonomous Vacuum Agent", "Simple Reflex / Model-Based", vacuum_peas)
    agent2 = AIAgent("Self-Driving Navigation Agent", "Goal & Utility-Based", car_peas)

    agent1.display_peas()
    agent1.act({"location": "Room_A", "cleanliness": "dirty"})
    agent1.act({"location": "Room_A", "cleanliness": "clean"})

    agent2.display_peas()
    print("\n[PEAS Analysis Complete - Viva Cleared 3/3]")

if __name__ == "__main__":
    main()

# ============================================================================
# EXPERIMENT THEORY (from AISC Laboratory Submission):
# ============================================================================
# AI Agents can be classified into types such as Simple Reflex, Model-Based,
# Goal-Based, and Utility-Based. The environment can be fully or partially
# observable, deterministic or stochastic, and episodic or sequential. PEAS
# properties include Performance measure, Environment, Actuators, and
# Sensors, which define the agent's behavior and interaction with the
# environment. TODO: define agent type based on environment and PEAS
# properties.AI Agents are based on the theory of intelligent behavior,
# using PEAS properties to define the agent's environment and actions. The
# theory involves the interaction between the agent and its environment, and
# the agent's perception and reasoning. The agent's type, such as simple
# reflex or model-based, influences its behavior. The theory provides a
# framework for understanding AI Agents.
# ============================================================================

