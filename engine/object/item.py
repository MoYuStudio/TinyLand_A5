
import pygame

import drivers

class Item:
    def __init__(self,id,pos,size):
        self.id = id
        self.pos = pos
        self.size = size
        
        self.num = 1
        
        self.translucence = False
        
        yaml = drivers.yaml.yaml_driver.YamlDriver()
        self.config = yaml.read(read_file='data/engine/item.yml')
        
        self.assets = pygame.image.load(self.config['assets_original']+str(self.id)+'.png').convert_alpha()
        
        self.rect = self.assets.get_rect()
        self.width = self.rect.width
        
    def renderer(self,surface):
        if self.translucence == True:
            self.assets.set_alpha(48)
        if self.translucence == False:
            self.assets.set_alpha(255)
            
        surface.blit(self.assets, self.rect)
    
    def motion(self):
        self.motioning = False
        try:
            if pygame.mouse.get_pressed()[0] == True:
                if pygame.Rect.collidepoint(self.rect,pygame.mouse.get_pos()):
                    self.motioning = True
                    print('motioning')
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
                    print('clicking')
                    # pygame.mixer.Channel(1).play(pygame.mixer.Sound("assets/sound/effect/switch_001.ogg"))
                    # time.sleep(0.1)
        except:
            pass
        
        return self.clicking