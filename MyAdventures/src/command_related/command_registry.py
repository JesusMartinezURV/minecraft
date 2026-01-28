from typing import Dict
from command_dictionary import *

class CommandRegistry:
    
    _agents: Dict[str, AgentCommandSet] = {
        AgentNames.EXPLORER: EXPLORER_COMMANDS,
        AgentNames.BUILDER: BUILDER_COMMANDS,
        AgentNames.MINER: MINER_COMMANDS,
    }
    
    @classmethod
    def register_agent(cls, agent_commands: AgentCommandSet):
        cls._agents[agent_commands.agent_name] = agent_commands
    
    @classmethod
    def get_agent_commands(cls, agent_name: str):
        return cls._agents.get(agent_name)
    
    @classmethod
    def get_all_agents(cls):
        return list(cls._agents.keys())
    
    @classmethod
    def get_class_for_agent(cls, agent_name: str):
        agent_commands = cls._agents.get(agent_name)
        return agent_commands.agent_class_name if agent_commands else None
    
    @classmethod
    def validate_command(cls, agent_name: str, command_name: str):
        agent_commands = cls._agents.get(agent_name)
        if not agent_commands:
            return False
        return agent_commands.get_command(command_name) is not None
    
    @classmethod
    def parse_chat_command(cls, chat_input: str):

        parts = chat_input.strip().split(maxsplit=2)
        
        if len(parts) < 2:
            return None
        
        agent_name = parts[0]
        command_name = parts[1]
        args_string = parts[2] if len(parts) > 2 else ""
        
        if not cls.validate_command(agent_name, command_name):
            return None
        
        agent_commands = cls.get_agent_commands(agent_name)
        command_pattern = agent_commands.get_command(command_name)
        
        return {
            "agent": agent_name,
            "command": command_name,
            "args": args_string,
            "parsed_args": command_pattern.parse_args(args_string) if command_pattern else {},
            "pattern": command_pattern
        }



