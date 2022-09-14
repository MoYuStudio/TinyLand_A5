
import glob
import time

import pygame

import engine
import drivers

class Game:
    def __init__(self):
        self.window_size = pygame.display.get_surface().get_size()
        yaml_file = drivers.yaml.yaml_driver.YamlDriver()
        self.config = yaml_file.read(read_file='data/config.yml')
        self.block_data = yaml_file.read(read_file='data/block/data.yml')
        
        json_file = drivers.json.json_driver.JsonDriver(path='data/blockmap')
        self.map = json_file.read()
        
        # self.size = 1
        self.blockmap_low_size = 4
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
        
    def background(self):
        
        # surface = pygame.Surface((self.bg1_ract.width,self.bg1_ract.height)).convert_alpha()
        # surface.fill((0,0,0,0))
        # surface.blit(self.bg1,(-self.blockmap_offset[0]+self.window_size[0]/4,-self.blockmap_offset[1]+self.window_size[1]/4))
        # surface = pygame.transform.scale(surface,(self.bg1_ract.width*self.blockmap_low_size, self.bg1_ract.height*self.blockmap_low_size))
        
        surface = pygame.Surface((self.window_size[0],self.window_size[1])).convert_alpha()
        surface.fill((0,0,0,255))
        
        return surface
        
    def blockmap(self):
        start_time = time.time()
        
        surface = pygame.Surface((self.window_size[0]/self.blockmap_low_size,self.window_size[1]/self.blockmap_low_size)).convert_alpha()
        surface.fill((0,0,0,0))
        
        self.blockmap_obj.renderer(surface,self.blockmap_offset)
        
        surface = pygame.transform.scale(surface,(self.window_size[0],self.window_size[1]))
        
        # print('1   '+str(time.time()-start_time))
        
        return surface

    def gui(self):
        
        surface = pygame.Surface((self.window_size[0],self.window_size[1])).convert_alpha()
        surface.fill((0,0,0,0))
        
        # self.blockmap_obj.block_motion_on
        
        choose_block_original = pygame.image.load('assets/block/'+str(self.blockmap_obj.block_motion_on)+'.png').convert_alpha()
        choose_block = pygame.transform.scale(choose_block_original,(16*self.config['ui_size']/2, 16*self.config['ui_size']/2))
        
        choose_block_name_font = pygame.font.Font('assets/font/kenney_pixel.ttf', 7*self.config['ui_size'])
        choose_block_name = choose_block_name_font.render(self.block_data[self.blockmap_obj.block_motion_on]['name'], True, (255,255,255))
        
        surface.blit(choose_block, (self.window_size[0]/(16*self.config['ui_size']),self.window_size[1]/(9*self.config['ui_size'])))
        surface.blit(choose_block_name, ((self.window_size[0]/(16*self.config['ui_size']))+(self.window_size[0]/(6*self.config['ui_size'])),self.window_size[1]/(6*self.config['ui_size'])))
        
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
                if self.event.key == pygame.K_q:
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
                if self.event.key == pygame.K_e:
                    self.backpack_menu_active = False