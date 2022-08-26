
import pygame

import engine
import scene

import drivers

class Game:
    def __init__(self):
        self.window_size = pygame.display.get_surface().get_size()
        yaml_file = drivers.yaml.yaml_driver.YamlDriver()
        self.config = yaml_file.read(read_file='data/scene/game.yml')
        
        json_file = drivers.json.json_driver.JsonDriver(path='data/blockmap')
        self.map = json_file.read()
        
        self.size = 4
        self.blockmap_obj = engine.blockmap.Blockmap(self.map['1'],self.size)
        
        self.blockmap_offset = [self.window_size[0]/self.size/2,self.window_size[1]/self.size/2]
        self.move_speed = 3
        self.move_up = False
        self.move_down = False
        self.move_left = False
        self.move_right = False
        
        self.block_pick = 4
    
    def renderer(self):
        
        if self.move_up == True:
            self.blockmap_offset[1] -= self.move_speed
        if self.move_down == True:
            self.blockmap_offset[1] += self.move_speed
        if self.move_left == True:
            self.blockmap_offset[0] -= self.move_speed
        if self.move_right == True:
            self.blockmap_offset[0] += self.move_speed
        
        surface = pygame.Surface((self.window_size[0],self.window_size[1])).convert_alpha()
        surface.fill((0,0,0,0))
        
        self.blockmap_obj.renderer(surface,self.blockmap_offset)
        
        return surface
    
    def scene_event(self,event):
        self.event = event
        
        if self.event.type == pygame.MOUSEMOTION:
            self.blockmap_obj.motion(pos_offset=self.blockmap_offset)
        
        if self.event.type == pygame.MOUSEBUTTONDOWN:
            self.blockmap_obj.touch(self.block_pick, pos_offset=self.blockmap_offset)
        
        if self.event.type == pygame.KEYDOWN:
            if self.event.key == pygame.K_UP or self.event.key == pygame.K_w:
                self.move_up = True
            if self.event.key == pygame.K_DOWN or self.event.key == pygame.K_s:
                self.move_down = True
            if self.event.key == pygame.K_LEFT or self.event.key == pygame.K_a:
                self.move_left = True
            if self.event.key == pygame.K_RIGHT or self.event.key == pygame.K_d:
                self.move_right = True
                
        if self.event.type == pygame.KEYUP:
            if self.event.key == pygame.K_UP or self.event.key == pygame.K_w:
                self.move_up = False
            if self.event.key == pygame.K_DOWN or self.event.key == pygame.K_s:
                self.move_down = False
            if self.event.key == pygame.K_LEFT or self.event.key == pygame.K_a:
                self.move_left = False
            if self.event.key == pygame.K_RIGHT or self.event.key == pygame.K_d:
                self.move_right = False