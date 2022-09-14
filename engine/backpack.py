
import pygame

import drivers

import engine.object as object

class Backpack:
    def __init__(self,item_size):
        self.item_size = item_size
        
        self.window_size = pygame.display.get_surface().get_size()
        
        self.display_size = [7,5]
        self.safe_zoom = 64
        self.gap_num = [(self.window_size[0]-self.safe_zoom*2)//self.display_size[0],(self.window_size[1]-self.safe_zoom*2)//self.display_size[1]]
        self.item_list = {}
        
        yaml = drivers.yaml.yaml_driver.YamlDriver()
        try:
            self.backpack_data = yaml.read(read_file='data/player/backpack.yml')
        except:
            pass
        
        timer = 0
        for y in range(self.display_size[1]):
            for x in range(self.display_size[0]):
                
                try:
                    if self.backpack_data[timer] != None:
                        self.item_list[str(x)+'_'+str(y)] = object.item.Item(self.backpack_data[timer]['id'],self.backpack_data[timer]['num'],[x*self.gap_num[0]+self.safe_zoom,y*self.gap_num[1]+self.safe_zoom],self.item_size)
                except:
                    pass
                
                timer += 1
        
    def renderer(self,surface):
        self.surface = surface
        
        for item in self.item_list:
            self.item_list[item].renderer(self.surface)
    
    def motion(self):
        for item in self.item_list:
            self.item_list[item].motion()
    
    def touch(self):
        for item in self.item_list:
            self.item_list[item].touch()