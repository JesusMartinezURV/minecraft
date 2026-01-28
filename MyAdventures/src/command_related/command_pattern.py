from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional

@dataclass
class CommandPattern:
    command_name: str
    args_schema: Dict[str, Any]
    description: str
    example: str
    
    def parse_args(self, arg_string: str):
        return {"raw": arg_string}


@dataclass
class AgentCommandSet:
    agent_name: str
    agent_class_name: str 
    commands: List[CommandPattern] = field(default_factory=list)
    
    def get_command(self, command_name: str):
        for cmd in self.commands:
            if cmd.command_name == command_name:
                return cmd
        return None
    
    def list_commands(self):
        return [cmd.command_name for cmd in self.commands]


