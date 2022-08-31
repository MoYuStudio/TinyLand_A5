
import glob

import pygame

import engine
import drivers

class Game:
    def __init__(self):
        self.window_size = pygame.display.get_surface().get_size()
        yaml_file = drivers.yaml.yaml_driver.YamlDriver()
        self.config = yaml_file.read(read_file='data/scene/game.yml')
        self.block_data = yaml_file.read(read_file='data/block/data.yml')
        
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
        
        self.bg1 = pygame.image.load('assets/background/0.png')
        self.bg1_ract = self.bg1.get_rect()
        
        self.block_pick_menu_active = True
        
    def background(self):
        
        surface = pygame.Surface((self.bg1_ract.width,self.bg1_ract.height)).convert_alpha()
        surface.fill((0,0,0,0))
        surface.blit(self.bg1,(-self.blockmap_offset[0],-self.blockmap_offset[1]))
        surface = pygame.transform.scale(surface,(self.bg1_ract.width*self.size, self.bg1_ract.height*self.size))
        
        return surface
        
    def blockmap(self):
        
        surface = pygame.Surface((self.window_size[0],self.window_size[1])).convert_alpha()
        surface.fill((0,0,0,0))
        
        self.blockmap_obj.renderer(surface,self.blockmap_offset)
        
        return surface

    def gui(self):
        
        surface = pygame.Surface((self.window_size[0],self.window_size[1])).convert_alpha()
        surface.fill((0,0,0,0))
        
        # self.blockmap_obj.block_motion_on
        
        choose_block_original = pygame.image.load('assets/block/'+str(self.blockmap_obj.block_motion_on)+'.png').convert_alpha()
        choose_block = pygame.transform.scale(choose_block_original,(16*self.size/2, 16*self.size/2))
        
        choose_block_name_font = pygame.font.Font('assets/font/kenney_pixel.ttf', 32)
        choose_block_name = choose_block_name_font.render(self.block_data[self.blockmap_obj.block_motion_on]['name'], True, (255,255,255))
        
        surface.blit(choose_block, (self.window_size[0]/(16*self.size),self.window_size[1]/(9*self.size)))
        surface.blit(choose_block_name, ((self.window_size[0]/(16*self.size))+(self.window_size[0]/(5*self.size)),self.window_size[1]/(9*self.size)))
        
        return surface
    
    def block_pick_menu(self):
        
        surface = pygame.Surface((self.window_size[0]/self.size,self.window_size[1]/self.size)).convert_alpha()
        surface.fill((0,0,0,0))
        
        surface.fill((0,0,0,128))
        
        surface = pygame.transform.scale(surface,(self.window_size[0], self.window_size[1]))
        
        block_list = []
        for filename in glob.glob(r'assets/block/*.png'):
            block_list.append(filename)
        
        x,y = 0,0
        for block in block_list:
            block_original = pygame.image.load(block)
            block = pygame.transform.scale(block_original,(16*self.size/2, 16*self.size/2))
            surface.blit(block,(100+x*(64),100+y*(64)))
            if x == 6:
                x = 0
                y += 1
            x+=1
            
            # surface.blit(self.tile_assets[i],(i*16,100))
            
        return surface
        
    def renderer(self):
        
        if self.move_up == True:
            self.blockmap_offset[1] -= self.move_speed
        if self.move_down == True:
            self.blockmap_offset[1] += self.move_speed
        if self.move_left == True:
            self.blockmap_offset[0] -= self.move_speed
        if self.move_right == True:
            self.blockmap_offset[0] += self.move_speed
            
        
        scene = pygame.Surface((self.window_size[0],self.window_size[1])).convert_alpha()
        scene.fill((0,0,0,0))
        
        scene.blit(self.background(),(0,0))
        scene.blit(self.blockmap(),(0,0))
        scene.blit(self.gui(),(0,0))
        
        if self.block_pick_menu_active == True:
            scene.blit(self.block_pick_menu(),(0,0))
        
        return scene
    
    def scene_event(self,event):
        self.event = event
        
        if self.block_pick_menu_active == False:
        
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
                    self.block_pick_menu_active = True
                    
            if self.event.type == pygame.KEYUP:
                if self.event.key == pygame.K_UP or self.event.key == pygame.K_w:
                    self.move_up = False
                if self.event.key == pygame.K_DOWN or self.event.key == pygame.K_s:
                    self.move_down = False
                if self.event.key == pygame.K_LEFT or self.event.key == pygame.K_a:
                    self.move_left = False
                if self.event.key == pygame.K_RIGHT or self.event.key == pygame.K_d:
                    self.move_right = False
                    
        if self.block_pick_menu_active == True:
            if self.event.type == pygame.KEYDOWN:
                if self.event.key == pygame.K_e:
                    self.block_pick_menu_active = False