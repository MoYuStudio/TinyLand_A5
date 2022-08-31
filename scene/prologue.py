
import pygame

import engine
import scene
import drivers


class Prologue:
    def __init__(self):
        self.window_size = pygame.display.get_surface().get_size()
        
        self.scene_switch = None
    
    def renderer(self):
        scene = pygame.Surface((self.window_size[0],self.window_size[1])).convert_alpha()
        scene.fill((0,0,0,0))
        
        icon_original = pygame.image.load('assets/icon/steam_title_icon_fin.png').convert_alpha()
        # icon = pygame.transform.scale(icon_original,(16*self.size/2, 16*self.size/2))
        
        scene.blit(icon_original, (0,0))

        self.scene_switch = 'game'
        
        return scene
    
    def scene_event(self,event):
        self.event = event