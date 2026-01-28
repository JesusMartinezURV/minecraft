import pkgutil
import importlib
import src.agents
from src.agents.base_agent import BaseAgent


def discover_agents():
    # Import all modules in agents package
    for _, module_name, _ in pkgutil.iter_modules(src.agents.__path__):
        importlib.import_module(f"{src.agents.__name__}.{module_name}")

    # Collect subclasses
    agents_list = []
    for cls in BaseAgent.__subclasses__():
        agents_list.append(cls)

    return agents_list

if __name__ == "__main__":
    agents = discover_agents()

    print("Discovered agents:")
    for agent_cls in agents:
        agent = agent_cls()
        print(f"- {agent.__class__.__name__}")
