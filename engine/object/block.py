
import pygame

import drivers

class Block:
    def __init__(self,id,pos):
        self.id = id
        self.pos = pos
        
        self.size = 1
        self.offset = [0,0]
        
        self.render_id = self.id
        
        yaml = drivers.yaml.yaml_driver.YamlDriver()
        self.config = yaml.read(read_file='data/engine/block.yml')
        
        try:
            self.block_data = yaml.read(read_file=self.config['block_data'])
        except:
            print('Engine/Object: Block (block_data) Missing')
            pass
        
    def timer(self):
        pass
    
    def renderer(self):
        try:
            self.assets_original = pygame.image.load(self.config['assets_original']+str(self.render_id)+'.png')
            self.assets = pygame.transform.scale(self.assets_original,(16*self.size, 16*self.size))
            
            self.rect = self.assets.get_rect()
            self.width = self.rect.width
        except:
            pass
            
    
    def motion(self):
        pass
    
    def touch(self):
        pass
    