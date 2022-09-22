
import glob
import time

import pygame

import engine
import drivers

class Game:
    def __init__(self):
        self.window_size = pygame.display.get_surface().get_size()
        
        self.yaml_file = drivers.yaml.yaml_driver.YamlDriver()
        self.config = self.yaml_file.read(read_file='data/config.yml')
        self.block_data = self.yaml_file.read(read_file='data/block/data.yml')
        
        
        json_file = drivers.json.json_driver.JsonDriver(path='data/blockmap')
        self.map = json_file.read()
        
        # self.size = 1
        self.blockmap_low_size = 5
        self.blockmap_obj = engine.blockmap.Blockmap(self.map['1'],self.blockmap_low_size)
        
        self.blockmap_offset = [self.window_size[0]/2/self.blockmap_low_size,self.window_size[1]/2/self.blockmap_low_size]
        self.move_speed = 3
        self.move_up = False
        self.move_down = False
        self.move_left = False
        self.move_right = False
        
        self.block_pick = 257
        
        self.bg1 = pygame.image.load('assets/background/0.png')
        self.bg1_ract = self.bg1.get_rect()
        
        self.backpack_menu_active = False
        
        self.backpack_obj = engine.backpack.Backpack(5)
        
        # self.input_map_original = pygame.image.load('assets/ui/game/input_map.png').convert_alpha()
        # self.input_map = pygame.transform.scale(self.input_map_original,(64*self.config['ui_size']/2, 64*self.config['ui_size']/2))
        
        self.topleft_infoboard_original = pygame.image.load('assets/ui/game/topleft_infoboard.png').convert_alpha()
        self.topleft_infoboard = pygame.transform.scale(self.topleft_infoboard_original,(64*self.config['ui_size']/2, 64*self.config['ui_size']/2))
        self.topleft_infoboard_font = pygame.font.Font('assets/font/kenney_pixel.ttf', 7*self.config['ui_size'])
        
        self.button_blockboard_original = pygame.image.load('assets/ui/game/button_blockboard.png').convert_alpha()
        self.button_blockboard = pygame.transform.scale(self.button_blockboard_original,(320*self.config['ui_size']/2, 32*self.config['ui_size']/2))
        self.button_blockboard_2_original = pygame.image.load('assets/ui/game/button_blockboard_2.png').convert_alpha()
        self.button_blockboard_2 = pygame.transform.scale(self.button_blockboard_2_original,(320*self.config['ui_size']/2, 32*self.config['ui_size']/2))
        
        self.land_icon_original = pygame.image.load('assets/block/1.png').convert_alpha()
        self.land_icon = pygame.transform.scale(self.land_icon_original,(16*self.config['ui_size']/2, 16*self.config['ui_size']/2))
        self.farm_icon_original = pygame.image.load('assets/block/261.png').convert_alpha()
        self.farm_icon = pygame.transform.scale(self.farm_icon_original,(16*self.config['ui_size']/2, 16*self.config['ui_size']/2))
        self.factory_icon_original = pygame.image.load('assets/block/512.png').convert_alpha()
        self.factory_icon = pygame.transform.scale(self.factory_icon_original,(16*self.config['ui_size']/2, 16*self.config['ui_size']/2))
        self.infrastructure_icon_original = pygame.image.load('assets/ui/game/infrastructure_icon.png').convert_alpha()
        self.infrastructure_icon = pygame.transform.scale(self.infrastructure_icon_original,(16*self.config['ui_size']/2, 16*self.config['ui_size']/2))
        self.land_icon_ui = engine.object.ui.UI()
        self.farm_icon_ui = engine.object.ui.UI()
        self.factory_icon_ui = engine.object.ui.UI()
        self.infrastructure_icon_ui = engine.object.ui.UI()
        
        # farm_icon
        self.farmland_ui = engine.object.ui.UI()
        
        self.land_menu_switch,self.farm_menu_switch,self.factory_menu_switch,self.infrastructure_menu_switch = False,False,False,False
        
    def background(self):
        
        # surface = pygame.Surface((self.bg1_ract.width,self.bg1_ract.height)).convert_alpha()
        # surface.fill((0,0,0,0))
        # surface.blit(self.bg1,(-self.blockmap_offset[0]+self.window_size[0]/4,-self.blockmap_offset[1]+self.window_size[1]/4))
        # surface = pygame.transform.scale(surface,(self.bg1_ract.width*self.blockmap_low_size, self.bg1_ract.height*self.blockmap_low_size))
        
        surface = pygame.Surface((self.window_size[0],self.window_size[1])).convert_alpha()
        surface.fill((0,0,0,255))
        
        return surface
        
    def blockmap(self):
        # start_time = time.time()
        
        surface = pygame.Surface((self.window_size[0]/self.blockmap_low_size,self.window_size[1]/self.blockmap_low_size)).convert_alpha()
        surface.fill((0,0,0,0))
        
        self.blockmap_obj.renderer(surface,self.blockmap_offset)
        
        surface = pygame.transform.scale(surface,(self.window_size[0],self.window_size[1]))
        
        # print('1   '+str(time.time()-start_time))
        
        return surface

    def gui(self):
        
        self.player_data = self.yaml_file.read(read_file='data/player/data.yml')
        
        surface = pygame.Surface((self.window_size[0],self.window_size[1])).convert_alpha()
        surface.fill((0,0,0,0))
        
        # self.blockmap_obj.block_motion_on
        
        # choose_block_original = pygame.image.load('assets/block/'+str(self.blockmap_obj.block_motion_on)+'.png').convert_alpha()
        # choose_block = pygame.transform.scale(choose_block_original,(16*self.config['ui_size']/2, 16*self.config['ui_size']/2))
        
        # choose_block_name_font = pygame.font.Font('assets/font/kenney_pixel.ttf', 7*self.config['ui_size'])
        # if self.block_data[self.blockmap_obj.block_motion_on]['name'] != 'air':
        #     choose_block_name = choose_block_name_font.render(self.block_data[self.blockmap_obj.block_motion_on]['name'], True, (255,255,255))
        # else:
        #     choose_block_name = choose_block_name_font.render('', True, (255,255,255))
        
        topleft_infoboard_development_point = self.topleft_infoboard_font.render(str(self.player_data['development_point']), True, (255,255,255))
        topleft_infoboard_population = self.topleft_infoboard_font.render(str(self.player_data['population']), True, (255,255,255))
        topleft_infoboard_money = self.topleft_infoboard_font.render(str(self.player_data['money']), True, (255,255,255))
        
        # surface.blit(self.input_map, ((self.window_size[0]-64*self.config['ui_size']/2,self.window_size[1]-64*self.config['ui_size']/2)))
        
        # surface.blit(choose_block, (4*self.config['ui_size'],self.window_size[1]-(16*self.config['ui_size'])))
        # surface.blit(choose_block_name, (16*self.config['ui_size'],self.window_size[1]-(16*self.config['ui_size'])))
        
        surface.blit(self.topleft_infoboard, ((0,0)))
        surface.blit(topleft_infoboard_development_point, (16*self.config['ui_size']/2,16*1*self.config['ui_size']/2))
        surface.blit(topleft_infoboard_population, (16*self.config['ui_size']/2,16*2*self.config['ui_size']/2))
        surface.blit(topleft_infoboard_money, (16*self.config['ui_size']/2,16*3*self.config['ui_size']/2))
        
        surface.blit(self.button_blockboard, (self.window_size[0]/2-(320*self.config['ui_size']/2)/2,self.window_size[1]-32*self.config['ui_size']/2))
        
        if self.land_menu_switch == True:
            surface.blit(self.button_blockboard_2, (self.window_size[0]/2-(320*self.config['ui_size']/2)/2,self.window_size[1]-2*32*self.config['ui_size']/2))
        if self.farm_menu_switch == True:
            surface.blit(self.button_blockboard_2, (self.window_size[0]/2-(320*self.config['ui_size']/2)/2,self.window_size[1]-2*32*self.config['ui_size']/2))
            self.farmland_ui.image_button_renderer(surface,self.farm_icon,pos=[self.window_size[0]/2-(320*self.config['ui_size']/2)/2 + 4*self.config['ui_size'] + 0*11.5*self.config['ui_size'],self.window_size[1]-2*32*self.config['ui_size']/2+6*self.config['ui_size']])
        if self.factory_menu_switch == True:
            surface.blit(self.button_blockboard_2, (self.window_size[0]/2-(320*self.config['ui_size']/2)/2,self.window_size[1]-2*32*self.config['ui_size']/2))
        if self.infrastructure_menu_switch == True:
            surface.blit(self.button_blockboard_2, (self.window_size[0]/2-(320*self.config['ui_size']/2)/2,self.window_size[1]-2*32*self.config['ui_size']/2))
        
        # surface.blit(self.land_icon, (self.window_size[0]/2-(320*self.config['ui_size']/2)/2 + 44*self.config['ui_size'], self.window_size[1]-32*self.config['ui_size']/2 + 4.5*self.config['ui_size']))
        # surface.blit(self.farm_icon, (self.window_size[0]/2-(320*self.config['ui_size']/2)/2 + 44*self.config['ui_size'] + 1*11.5*self.config['ui_size'], self.window_size[1]-32*self.config['ui_size']/2 + 4.5*self.config['ui_size']))
        # surface.blit(self.factory_icon, (self.window_size[0]/2-(320*self.config['ui_size']/2)/2 + 44*self.config['ui_size'] + 2*11.5*self.config['ui_size'], self.window_size[1]-32*self.config['ui_size']/2 + 4.5*self.config['ui_size']))
        # surface.blit(self.infrastructure_icon, (self.window_size[0]/2-(320*self.config['ui_size']/2)/2 + 44*self.config['ui_size'] + 3*11.5*self.config['ui_size'], self.window_size[1]-32*self.config['ui_size']/2 + 4.5*self.config['ui_size']))
        
        self.land_icon_ui.image_button_renderer(surface,self.land_icon,pos=[self.window_size[0]/2-(320*self.config['ui_size']/2)/2 + 44*self.config['ui_size'], self.window_size[1]-32*self.config['ui_size']/2 + 4.5*self.config['ui_size']])
        self.farm_icon_ui.image_button_renderer(surface,self.farm_icon,pos=[self.window_size[0]/2-(320*self.config['ui_size']/2)/2 + 44*self.config['ui_size'] + 1*11.5*self.config['ui_size'], self.window_size[1]-32*self.config['ui_size']/2 + 4.5*self.config['ui_size']])
        self.factory_icon_ui.image_button_renderer(surface,self.factory_icon,pos=[self.window_size[0]/2-(320*self.config['ui_size']/2)/2 + 44*self.config['ui_size'] + 2*11.5*self.config['ui_size'], self.window_size[1]-32*self.config['ui_size']/2 + 4.5*self.config['ui_size']])
        self.infrastructure_icon_ui.image_button_renderer(surface,self.infrastructure_icon,pos=[self.window_size[0]/2-(320*self.config['ui_size']/2)/2 + 44*self.config['ui_size'] + 3*11.5*self.config['ui_size'], self.window_size[1]-32*self.config['ui_size']/2 + 4.5*self.config['ui_size']])
        
        return surface
    
    def backpack_menu(self):
        
        surface = pygame.Surface((self.window_size[0],self.window_size[1])).convert_alpha()
        surface.fill((0,0,0,0))
        
        surface.fill((0,0,0,128))
        
        self.backpack_obj.renderer(surface)
            
        return surface
        
    def renderer(self):
        
        if self.move_up == True:
            self.blockmap_offset[1] += self.move_speed
        if self.move_down == True:
            self.blockmap_offset[1] -= self.move_speed
        if self.move_left == True:
            self.blockmap_offset[0] += self.move_speed
        if self.move_right == True:
            self.blockmap_offset[0] -= self.move_speed
            
        
        scene = pygame.Surface((self.window_size[0],self.window_size[1])).convert_alpha()
        scene.fill((0,0,0,0))
        
        scene.blit(self.background(),(0,0))
        scene.blit(self.blockmap(),(0,0))
        scene.blit(self.gui(),(0,0))
        
        if self.backpack_menu_active == True:
            scene.blit(self.backpack_menu(),(0,0))
        
        return scene
    
    def scene_event(self,event):
        self.event = event
        
        if self.backpack_menu_active == False:
        
            if self.event.type == pygame.MOUSEMOTION:
                self.blockmap_obj.motion(pos_offset=self.blockmap_offset)
            
            if self.event.type == pygame.MOUSEBUTTONDOWN:
                button_blockboard_switch = False
                try:
                    if self.land_icon_ui.touch() == True:
                        print('land_icon_ui')
                        button_blockboard_switch = True
                        if self.land_menu_switch == True:
                            self.land_menu_switch = False
                        elif self.land_menu_switch == False:
                            self.land_menu_switch,self.farm_menu_switch,self.factory_menu_switch,self.infrastructure_menu_switch = True,False,False,False
                except:
                    pass
                try:
                    if self.farm_icon_ui.touch() == True:
                        print('farm_icon_ui')
                        button_blockboard_switch = True
                        if self.farm_menu_switch == True:
                            self.farm_menu_switch = False
                        elif self.farm_menu_switch == False:
                            self.land_menu_switch,self.farm_menu_switch,self.factory_menu_switch,self.infrastructure_menu_switch = False,True,False,False
                except:
                    pass
                try:
                    if self.factory_icon_ui.touch() == True:
                        print('factory_icon_ui')
                        button_blockboard_switch = True
                        if self.factory_menu_switch == True:
                            self.factory_menu_switch = False
                        elif self.factory_menu_switch == False:
                            self.land_menu_switch,self.farm_menu_switch,self.factory_menu_switch,self.infrastructure_menu_switch = False,False,True,False
                except:
                    pass
                try:
                    if self.infrastructure_icon_ui.touch() == True:
                        print('infrastructure_icon_ui')
                        button_blockboard_switch = True
                        if self.infrastructure_menu_switch == True:
                            self.infrastructure_menu_switch = False
                        elif self.infrastructure_menu_switch == False:
                            self.land_menu_switch,self.farm_menu_switch,self.factory_menu_switch,self.infrastructure_menu_switch = False,False,False,True
                except:
                    pass
            
                if button_blockboard_switch == False:
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
                    
            if self.event.type == pygame.KEYDOWN:
                if self.event.key == pygame.K_b:
                    self.backpack_menu_active = True
                if self.event.key == pygame.K_r:
                    print('reset the perlin noise map ...')
                    self.blockmap_obj.perlin_noise_set()
                    
            if self.event.type == pygame.KEYUP:
                if self.event.key == pygame.K_UP or self.event.key == pygame.K_w:
                    self.move_up = False
                if self.event.key == pygame.K_DOWN or self.event.key == pygame.K_s:
                    self.move_down = False
                if self.event.key == pygame.K_LEFT or self.event.key == pygame.K_a:
                    self.move_left = False
                if self.event.key == pygame.K_RIGHT or self.event.key == pygame.K_d:
                    self.move_right = False
                    
        if self.backpack_menu_active == True:
            if self.event.type == pygame.MOUSEMOTION:
                self.backpack_obj.motion()
            
            if self.event.type == pygame.MOUSEBUTTONDOWN:

                self.backpack_obj.touch()
                self.block_pick = self.backpack_obj.bpk_id

                
            if self.event.type == pygame.KEYDOWN:
                if self.event.key == pygame.K_ESCAPE:
                    self.backpack_menu_active = False