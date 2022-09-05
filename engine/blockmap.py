
import time
import random
import queue
import threading

import noise

import engine.object as object

class Blockmap:
    def __init__(self,map,block_size):
        
        self.map = self.perlin_noise_set()
        self.block_size = block_size
        
        self.block_motion_on = 0
        
        self.block_list = {}
        self.block_pos_list = {}
        
        self.translucence_mod = None
        self.translucence_id_list = ['0_0_0']
        
        for y in self.map:
            for x in range(len(self.map[y])):
                for z in range(len(self.map[y][x])):
                    block_pos = {'x':int(x),'y':int(y),'z':int(z)}
                    block_id = self.map[y][x][z]
                    self.block_list[str(x)+'_'+str(y)+'_'+str(z)] = object.block.Block(block_id,block_pos,self.block_size)
                    self.block_pos_list[str(x)+'_'+str(y)+'_'+str(z)] = block_pos
    
        self.block_list_iter = iter(self.block_list)
    
    def perlin_noise_set(self):
        map_boarder = 32
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
        
        start_time = time.time()
        
        key = list(self.block_list.keys())
        key_num = int(len(key))
        key_num = key_num//9
        num = 21
        
        key_1 = key[0:num*2]
        key_2 = key[num*2:num*4]
        key_3 = key[num*4:num*6]
        key_4 = key[num*6:num*8]
        
        threadLock = threading.Lock()
        threads = []
        
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
        
        t1 = threading.Thread(target=thr, args=(key_1,))
        t2 = threading.Thread(target=thr, args=(key_2,))
        t3 = threading.Thread(target=thr, args=(key_3,))
        t4 = threading.Thread(target=thr, args=(key_4,))

        t1.start()
        t2.start()
        t3.start()
        t4.start()

        # 添加线程到线程列表
        threads.append(t1)
        threads.append(t2)
        threads.append(t3)
        threads.append(t4)

        # 等待所有线程完成
        for t in threads:
            t.join()
        
        print('1   '+str(time.time()-start_time))
            
    def touch(self,change_block,pos_offset=[0,0]):
        for block in self.block_list:
            self.block_list[block].offset = pos_offset
            self.block_list[block].touch(change_block)
            
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