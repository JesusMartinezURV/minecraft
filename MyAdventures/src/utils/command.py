from src.utils.singleton import Singleton
from mcpi.minecraft import Minecraft
import mcpi.block as block


class MinecraftWorld(metaclass=Singleton):
    
    def __init__ (self):
        mc = Minecraft.create()
    

    
