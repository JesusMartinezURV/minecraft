from src.utils.singleton import Singleton
from logging.handlers import RotatingFileHandler
import logging


class Logger(metaclass=Singleton):

    def __init__(self):
        self.logger = logging.getLogger("Logger")
        self.logger.setLevel(logging.DEBUG)
        self.logger.propagate = False

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"  
        )

        console = logging.StreamHandler()
        console.setFormatter(formatter)
        self.logger.addHandler(console)
        
        # File handler
        file_h = RotatingFileHandler("events.log", maxBytes=5_000_000, backupCount=3)
        file_h.setFormatter(formatter)
        self.logger.addHandler(file_h)

    
    def log_debug(self, author, action, debug_message):
        self.logger.debug(f"[{author}] {action}: {debug_message}")

    def log_error(self, author, action, context_message):
        self.logger.error(f"[{author}] {action}: {context_message}")
    
    def log_info(self, author, action, context_message):
        self.logger.info(f"[{author}] {action}: {context_message}")
