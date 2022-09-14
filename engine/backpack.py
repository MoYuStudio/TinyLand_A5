
import pygame

import engine.object as object

class Backpack:
    def __init__(self,item_size):
        self.item_size = item_size
        
        self.window_size = pygame.display.get_surface().get_size()
        
        # for y in self.map:
        #     for x in range(len(self.map[y])):
        #         self.block_list[str(x)+'_'+str(y)+'_'+str(z)] = object.block.Block(block_id,block_pos,self.block_size)#,self.block_assets
        
    def renderer(self,surface):
        self.surface = surface
    
    def motion(self):
        pass
    
    def touch(self):
        pass