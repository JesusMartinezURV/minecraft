
class AgentFactory:
    @staticmethod
    def create_agent(agent_type, agent_id):
        match agent_type:
            case "builder":
                return BuilderBot(agent_id)
            case "miner":
                return MinerBot(agent_id)
            case _:
                raise ValueError(f"Unknown agent type: {agent_type}")