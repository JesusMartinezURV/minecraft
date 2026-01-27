import asyncio
from src.utils.singleton import Singleton


class MessageBroker(metaclass=Singleton):
    def __init__(self):
        self.general_queue = asyncio.Queue()
        self.agent_queues = {}



    def add_agent():
        pass

    def input_messsage(message):
        pass

    def process_message():
    
    