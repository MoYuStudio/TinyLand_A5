
import engine.object as object

class Blockmap:
    def __init__(self,map,block_size):
        self.map = map
        self.block_size = block_size
        
        self.block_list = {}
        
        for y in self.map:
            for x in range(len(self.map[y])):
                for z in range(len(self.map[y][x])):
                    block_pos = {'x':x,'y':y,'z':z}
                    block_id = self.map[y][x][z]
                    self.block_list[str(x)+'_'+str(y)+'_'+str(z)] = object.block.Block(block_id,block_pos,self.block_size)
    
    def renderer(self,surface,pos_offset=[0,0]):
        self.surface = surface
        for block in self.block_list:
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