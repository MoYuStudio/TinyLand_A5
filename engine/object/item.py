
from tkinter import Button
import pygame

import drivers

class Item:
    def __init__(self,id,num,pos,size):
        self.id = id
        self.num = num
        self.pos = pos
        self.size = size
        
        yaml = drivers.yaml.yaml_driver.YamlDriver()
        self.config = yaml.read(read_file='data/engine/item.yml')
        
        self.assets = pygame.image.load(self.config['assets_original']+str(self.id)+'.png').convert_alpha()
        self.rect = self.assets.get_rect()
        self.width = self.rect.width
        self.assets = pygame.transform.scale(self.assets,((self.width*self.size,self.width*self.size)))
        self.rect = self.assets.get_rect()
        self.width = self.rect.width
        
        self.font = pygame.font.Font('assets/font/kenney_pixel.ttf', 12*self.size)
        
    def renderer(self,surface):
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]
        num_text = self.font.render(str(self.num), True, (255,255,255))
        surface.blit(self.assets, self.rect)
        surface.blit(num_text, self.rect)
    
    def motion(self):
        self.motioning = False
        
        try:
            if pygame.Rect.collidepoint(self.rect,pygame.mouse.get_pos()):
                self.motioning = True
                # print('motioning')
                # pygame.mixer.Channel(1).play(pygame.mixer.Sound("assets/sound/effect/switch_001.ogg"))
                # time.sleep(0.1)
        except:
            pass
        
        return self.motioning
    
    def touch(self):
        self.clicking = False
        try:
            if pygame.mouse.get_pressed()[0] == True:
                if pygame.Rect.collidepoint(self.rect,pygame.mouse.get_pos()):
                    self.clicking = True
                    # print('clicking')
                    # pygame.mixer.Channel(1).play(pygame.mixer.Sound("assets/sound/effect/switch_001.ogg"))
                    # time.sleep(0.1)
        except:
            pass
        
        return self.clicking