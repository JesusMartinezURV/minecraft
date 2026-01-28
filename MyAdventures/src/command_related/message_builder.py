from typing import Dict, List, Any, Optional
from datetime import datetime
from MyAdventures.src.command_related.command_registry import CommandRegistry



class MessageBuilder:
    @staticmethod
    def create_command_message(agent_name: str, command_name: str, payload: Dict[str, Any], source: str = "user"):
        return {
            "type": command_name,
            "source": source,
            "target": agent_name,
            "timestamp": datetime.now().isoformat(),
            "payload": payload,
            "context": []
        }
    
    @staticmethod
    def create_from_chat(chat_input: str):
        parsed = CommandRegistry.parse_chat_command(chat_input)
        
        if not parsed:
            return None
        
        return MessageBuilder.create_command_message(
            agent_name=parsed["agent"],
            command_name=parsed["command"],
            payload=parsed["parsed_args"],
            source="User"
        )
    
    @staticmethod
    def create_agent_to_agent_message(source_agent: str, target_agent: str, message_type: str, payload: Dict[str, Any]):
        return {
            "type": message_type,
            "source": source_agent,
            "target": target_agent,
            "timestamp": datetime.now().isoformat(),
            "payload": payload,
            "context": []
        }
    
    @staticmethod
    def create_broadcast_message(source_agent: str, message_type: str, payload: Dict[str, Any]):
        return {
            "type": message_type,
            "source": source_agent,
            "target": "ALL",  # Broadcast indicator
            "timestamp": datetime.now().isoformat(),
            "payload": payload,
            "context": []
        }
