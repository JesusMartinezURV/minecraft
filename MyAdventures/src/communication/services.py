from mailbox import Message
from MyAdventures.src.utils.minecraft_world import MinecraftWorld
from src.utils.dynamic_discovery import discover_agents
class ChatService:
    def __init__(self):
        self.mc = MinecraftWorld()
        agents_ids = discover_agents()
    
    async def poll_chat(self):
        raw_msgs = await self.mc.poll_chat_messages()
        constructed_msgs = []
        for m in raw_msgs:
            if m and self._validate_chat(m):
                constructed_msgs.append(self.construct_message(m))
        return constructed_msgs
