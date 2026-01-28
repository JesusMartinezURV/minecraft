from src.utils.singleton import Singleton
from mcpi.minecraft import Minecraft
import mcpi.block as block


class MinecraftWorld(metaclass=Singleton):
    
    def __init__ (self):
        self.mc = Minecraft.create()
    
    def get_player_position (self):
        return self.mc.player.getTilePos()
    
    def get_block_altitude (self, x, z):
        return self.mc.getHeight(x, z)
    
    def block_id (self, x, y, z):
        return self.mc.getBlock(x, y, z)
    
    def set_block (self, x, y, z, block_id):
        self.mc.setBlock(x, y, z, block_id)
    
    def is_block_wanted (self, x, y, z, wanted_block_id):
        return self.mc.getBlock(x, y, z) == wanted_block_id

    def post_message_chat (self, message):
        self.mc.postToChat(message)

    def poll_chat_messages (self):
        posts = []
        for post in self.mc.events.pollChatPosts(): 
            if post.message:
                posts.append(post.message)
        return posts