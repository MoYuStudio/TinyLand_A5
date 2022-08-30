
import engine.object as object

class Blockmap:
    def __init__(self,map,block_size):
        self.map = map
        self.block_size = block_size
        
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
    
    def renderer(self,surface,pos_offset=[0,0]):
        self.surface = surface
        for block in self.block_list:
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
            
    def touch(self,change_block,pos_offset=[0,0]):
        for block in self.block_list:
            self.block_list[block].offset = pos_offset
            self.block_list[block].touch(change_block)
            
    def motion(self,pos_offset=[0,0]):
        for block in self.block_list:
            self.block_list[block].offset = pos_offset
            self.block_list[block].motion()
            if self.block_list[block].motioning == True:
                for id in self.translucence_id_list:
                    try:
                        self.block_list[id].translucence = False
                    except:
                        pass
                self.translucence_mod = self.block_pos_list[block]