
import pygame

import engine.object as object

class Backpack:
    def __init__(self,item_size):
        self.item_size = item_size
        
        self.window_size = pygame.display.get_surface().get_size()
        
    def renderer(self,surface):
        pass
    
    def motion(self):
        pass
    
    def touch(self):
        pass