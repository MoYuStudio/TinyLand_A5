
import time
import pygame

class UI:
    def __init__(self,ui_type='text_button'):
        self.ui_type = ui_type
        self.ui_type_list = ['text_button']
        
        self.font_dict = {'kenney_pixel':[pygame.font.Font('tinyland/assets/font/kenney_pixel.ttf', size)for size in range(0,(128+1),1)]}
        
    def text_button_renderer(self,surface,text='text',pos=[0,0],color=(255,255,255),font_size=32,font_type='kenney_pixel'):

        self.button = self.font_dict[font_type][font_size].render(text, True, color)
        self.rect = self.button.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        
        surface.blit(self.button, self.rect)
        
    def image_button_renderer(self,surface,image,pos=[0,0]):
        
        self.button = image
        self.rect = self.button.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        surface.blit(self.button, self.rect)
    
    def touch(self):
        self.clicked = False
        try:
            if pygame.mouse.get_pressed()[0] == True:
                if pygame.Rect.collidepoint(self.rect,pygame.mouse.get_pos()):
                    self.clicked = True
                    # pygame.mixer.Channel(1).play(pygame.mixer.Sound("assets/sound/effect/switch_001.ogg"))
                    # time.sleep(0.1)
        except:
            pass
        
        return self.clicked
    