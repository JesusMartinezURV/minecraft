from abc import ABC, abstractmethod

class BaseAgent(ABC):

    def __init__(self):
        self.message

    @abstractmethod
    def perceive (self):
        pass
    
    @abstractmethod
    def decide (self):
        pass
    
    @abstractmethod
    def act (self):
        pass
    
    @abstractmethod
    def send_message (self):
        pass