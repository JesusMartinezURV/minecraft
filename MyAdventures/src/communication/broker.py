import asyncio
from src.agents.base_agent import BaseAgent
from src.utils.logging import Logger
from MyAdventures.src.utils.minecraft_world import MinecraftWorld
from src.utils.singleton import Singleton


class MessageBroker(metaclass=Singleton):
    def __init__(self):
        self.logger = Logger()
        self.mc = MinecraftWorld()

        self.message_queue = asyncio.Queue()
        self.agents = {}
    
    async def run(self):
        while True:
            # Concurrently handle multiple operations
            await asyncio.gather(
                self._poll_chat(),
                self._route_messages(),
                self._collect_agent_outputs()
            ) 

    async def _poll_chat(self):
        msgs = await self.mc.poll_chat_messages()
        for m in msgs:
            if m and self.validate_message(m):
                await self.message_queue.put(m)

    async def _route_messages(self):
        try:
            msg = self.message_queue.get_nowait()
            agent_id = msg.target
            await self.agents[agent_id].put(msg)
        except asyncio.QueueEmpty:
            pass

    def add_agent(self, name, agent : BaseAgent):
        self.agents[name] = agent

    def input_message(self, message):
        self.message_queue.put_nowait(message) 

    async def broadcast_messages(self):
        pass