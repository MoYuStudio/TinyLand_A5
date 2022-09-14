
import time
# import glob
import random
import threading

import noise
import pygame

import drivers

import engine.object as object

class Blockmap:
    def __init__(self,map,block_size):
        
        self.map = self.perlin_noise_set()
        self.block_size = block_size
        
        self.block_motion_on = 0
        # self.block_below = 0
        
        self.block_list = {}
        self.block_pos_list = {}
        
        self.translucence_mod = None
        self.translucence_id_list = ['0_0_0']
        
        for y in self.map:
            for x in range(len(self.map[y])):
                for z in range(len(self.map[y][x])):
                    block_pos = {'x':int(x),'y':int(y),'z':int(z)}
                    block_id = self.map[y][x][z]
                    self.block_pos_list[str(x)+'_'+str(y)+'_'+str(z)] = block_pos
                    self.block_list[str(x)+'_'+str(y)+'_'+str(z)] = object.block.Block(block_id,block_pos,self.block_size)#,self.block_assets
        
        yaml = drivers.yaml.yaml_driver.YamlDriver()
        try:
            self.block_data = yaml.read(read_file='data/block/data.yml')
        except:
            print('Engine/Object: Block (block_data) Missing')
            pass
    
    def perlin_noise_set(self):
        map_boarder = 16
        octaves = 2 #2
        freq = random.randint(5,10) #12
        map_seed = random.randint(100000, 999999)

        perlin_noise_map_list = [[int(noise.pnoise2((x/freq)+map_seed,(y/freq)+map_seed,octaves)*100+50) for x in range(0,map_boarder,1)] for y in range(0,map_boarder,1)]

        perlin_noise_map_0 = []
        perlin_noise_map_1 = []
        
        for x in range(len(perlin_noise_map_list)):
            perlin_noise_map_0.append([])
            perlin_noise_map_1.append([])
            for z in range(len(perlin_noise_map_list[x])):
                if -1000 <= perlin_noise_map_list[x][z] <= 37:
                    perlin_noise_map_0[x].append(5)
                    perlin_noise_map_1[x].append(0)
                elif 38 <= perlin_noise_map_list[x][z] <= 40:
                    perlin_noise_map_0[x].append(3)
                    perlin_noise_map_1[x].append(0)
                elif 41 <= perlin_noise_map_list[x][z] <= 65:
                    perlin_noise_map_0[x].append(1)
                    perlin_noise_map_1[x].append(0)
                elif 66 <= perlin_noise_map_list[x][z] <= 70:
                    perlin_noise_map_0[x].append(2)
                    perlin_noise_map_1[x].append(0)
                elif 70 <= perlin_noise_map_list[x][z] <= 1100:
                    perlin_noise_map_0[x].append(4)
                    perlin_noise_map_1[x].append(4)
                else:
                    perlin_noise_map_0[x].append(0)
                    perlin_noise_map_1[x].append(0)
        
        perlin_noise_map = {0:perlin_noise_map_0,1:perlin_noise_map_1}
        
        self.map = perlin_noise_map
        
        try:
            for y in self.map:
                for x in range(len(self.map[y])):
                    for z in range(len(self.map[y][x])):
                        block_pos = {'x':int(x),'y':int(y),'z':int(z)}
                        block_id = self.map[y][x][z]
                        self.block_list[str(x)+'_'+str(y)+'_'+str(z)] = object.block.Block(block_id,block_pos,self.block_size)
                        self.block_pos_list[str(x)+'_'+str(y)+'_'+str(z)] = block_pos
        except:
            pass
        
        return perlin_noise_map
            
    def renderer(self,surface,pos_offset=[0,0]):
        self.surface = surface
        
        threadLock = threading.Lock()
        threads = []
        threads_num = 4
        
        key = list(self.block_list.keys())
        key_num = int(len(key)/threads_num)
        key_t = []
        
        for i in range(threads_num):
            key_t_list = key[key_num*i:key_num*(i+1)]
            key_t.append(key_t_list)
            
        def thr(key_thr):
            threadLock.acquire()
            for block in key_thr:
                if self.block_pos_list[block] == self.translucence_mod:
                    t = self.translucence_mod
                    self.translucence_id_list = [str(t['x']+1)+'_'+str(t['y'])+'_'+str(t['z']),
                                                    str(t['x'])+'_'+str(t['y'])+'_'+str(t['z']+1),
                                                    str(t['x']+1)+'_'+str(t['y'])+'_'+str(t['z']+1)]
                    
                    for id in self.translucence_id_list:
                        try:
                            self.block_list[id].translucence = True
                        except:
                            pass
                
                self.block_list[block].offset = pos_offset
                self.block_list[block].renderer(self.surface)
            threadLock.release()
            
        t = {}
        for num in range(threads_num):
            t[num] = threading.Thread(target=thr, args=(key_t[num],))
            t[num].start()
            threads.append(t[num])

        for t in threads:
            t.join()
            
    def touch(self,change_block,pos_offset=[0,0]):
        for block in self.block_list:
            self.block_list[block].offset = pos_offset
            
            block_id = block.split('_', 3)
            try:
                if self.block_list[block_id[0]+'_0_'+block_id[2]].id in self.block_data[change_block]['buildable']:
                     self.block_list[block].touch(change_block)
            except:
                pass
            
    def motion(self,pos_offset=[0,0]):
        for block in self.block_list:
            self.block_list[block].offset = pos_offset
            self.block_list[block].motion()
            
            if self.block_list[block].motioning == True:
                self.block_motion_on = self.block_list[block].id
                
                for id in self.translucence_id_list:
                    try:
                        self.block_list[id].translucence = False
                    except:
                        pass
                self.translucence_mod = self.block_pos_list[block]