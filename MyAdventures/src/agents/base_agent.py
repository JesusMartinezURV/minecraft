import asyncio
from abc import ABC, abstractmethod
from src.reflection.states import State

class BaseAgent(ABC):
    agent_name: str = None

    def __init__(self):
        self.state = State.IDLE
        self.message_queue = asyncio.Queue()
    
    async def run(self):
        while True:
            match self.state:
                case State.IDLE:
                    await self._handle_idle()
                case State.RUNNING:
                    await self._execute_cycle()
                case State.PAUSED:
                    await self._handle_paused()
                case State.STOPPED:
                    await self._handle_stopped()
                case State.ERROR:
                    await self._handle_error()

    async def _execute_cycle(self):
        perception = await self._perceive()
        decision = await self._decide(perception)
        await self._act(decision)

        try: 
            cmd = self.message_queue.get_nowait()
            self._process_command(cmd)
        except asyncio.QueueEmpty:
            pass

    @abstractmethod
    def _perceive (self):
        return 
    
    @abstractmethod
    def _decide (self):
        pass
    
    @abstractmethod
    def _act (self):
        pass
    
