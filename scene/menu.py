
import random

import pygame

import engine
import scene
import drivers


class Menu:
    def __init__(self):
        self.window_size = pygame.display.get_surface().get_size()
        yaml_file = drivers.yaml.yaml_driver.YamlDriver()
        self.config = yaml_file.read(read_file='data/config.yml')
        
        self.bg1 = pygame.image.load('assets/background/0.png')
        self.bg1_ract = self.bg1.get_rect()
        
        self.tile0_small = pygame.image.load('assets/block/0.png')
        self.tile1_small = pygame.image.load('assets/block/512.png')
        self.tile0 = pygame.transform.scale(self.tile0_small,(16*self.config['ui_size']*2, 16*self.config['ui_size']*2))
        self.tile1 = pygame.transform.scale(self.tile1_small,(16*self.config['ui_size']*2, 16*self.config['ui_size']*2))
        self.tile1_rect = self.tile1.get_rect()
        
        self.tile1_ui = engine.object.ui.UI()
        
        self.timer = 0
        
        self.scene_switch = None
    
    def background(self):
        surface = pygame.Surface((self.bg1_ract.width,self.bg1_ract.height)).convert_alpha()
        surface.fill((0,0,0,0))
        surface.blit(self.bg1,(0,0))
        surface = pygame.transform.scale(surface,(self.bg1_ract.width*self.config['ui_size'], self.bg1_ract.height*self.config['ui_size']))
        
        return surface
    
    def renderer(self):
        
        scene = pygame.Surface((self.window_size[0],self.window_size[1])).convert_alpha()
        scene.fill((0,0,0,0))
        scene.blit(self.background(),(random.randint(10,20),random.randint(10,20)))
        
        self.timer += 1
        if self.timer//360>=1:
            self.timer = 0
        rot_rect = pygame.transform.rotate(self.tile1,self.timer)
        scene.blit(rot_rect,(self.window_size[0]/2-self.tile1_rect.width/2,self.window_size[1]/2-self.tile1_rect.height/2))
        self.tile1_ui.image_button_renderer(scene,self.tile0,pos=[self.window_size[0]/2-self.tile1_rect.width/2,self.window_size[1]/2-self.tile1_rect.height/2])
        
        return scene
    
    def scene_event(self,event):
        self.event = event
        
        if self.event.type == pygame.MOUSEBUTTONDOWN:
            try:
                if self.tile1_ui.touch() == True:
                    self.scene_switch = 'game'
            except:
                pass