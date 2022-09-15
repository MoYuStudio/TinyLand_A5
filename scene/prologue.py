
import time

import pygame

import engine
import scene
import drivers


class Prologue:
    def __init__(self):
        self.window_size = pygame.display.get_surface().get_size()
        
        yaml_file = drivers.yaml.yaml_driver.YamlDriver()
        self.config = yaml_file.read(read_file='data/config.yml')
        
        self.scene_switch = None
        
        self.logo_original = pygame.image.load('assets/icon/logo.png').convert_alpha()
        self.logo = pygame.transform.scale(self.logo_original,(16*self.config['ui_size'], 16*self.config['ui_size']))
        self.rect = self.logo.get_rect()
        self.wide = self.rect.width
        
        alpha=[]
        for a in range(0,450+1,1):
            alpha.append(a)
        self.alpha = iter(alpha)
        
        self.timer = 255
        
        self.sound_timer = 1
    
    def renderer(self):
        scene = pygame.Surface((self.window_size[0],self.window_size[1])).convert_alpha()
        scene.fill((0,0,0,0))
        
        alpha_num = next(self.alpha)
        
        if alpha_num >= 450:
            self.scene_switch = 'menu'
        
        if alpha_num > 300:
            self.timer -= 2
            alpha_num = self.timer
            
        if alpha_num > 255:
            alpha_num = 255
            if self.sound_timer != 0:
                pygame.mixer.Channel(1).play(pygame.mixer.Sound('assets/sound/kenney_interfacesounds/bong_001.ogg'))
                self.sound_timer -= 1

        self.logo.set_alpha(alpha_num)
        scene.blit(self.logo, ((self.window_size[0]/2)-self.wide/2,(self.window_size[1]/2)-self.wide/2))
        time.sleep(0.0001)
        
        return scene
    
    def scene_event(self,event):
        self.event = event