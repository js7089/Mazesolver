INF = 500

# The 'maze-map' data structure
# consists of actual 'array' and 'maze-size'
class Map():
    data = []
    size_x, size_y = 0, 0

    def __init__(self, array, maze_x, maze_y):
        self.data = array
        self.size_x, self.size_y = maze_x, maze_y

    # returns element of index (x,y) from maze
    def elem(self, i, j):
        return self.data[j*self.size_x + i]

    # set element 
    def set(self, i, j, value):
        self.data[j*self.size_x + i] = value
    
    def __str__(self):
        string_ = ""
        for j in range(self.size_y):
            for i in range(self.size_x):
                s = self.elem(i, j)
                if(s >=0 and s<10):
                    string_ += str(s)
                elif(s<0):
                    string_ += "-"
                else:
                    string_ += "#"
                #string_ += ("%s" %(s if (s<10 and s>0) else "#"))
            string_ += "\n"
        return string_

class Trace():
    trace = list()  # List of tuples<x,y>
    valid = 1;      # valid = 1, void = 0

    # Trace initialization
    def __init__(self, trace_i=[], valid_i=1):
        self.trace = trace_i
        self.valid = valid_i

    # Trace concatenation 
    def __add__(self, other):
        if( other== None):
            return Trace(self.trace, 0)
        new_trace_lst = self.trace + other.trace
#        new_trace_valid = 1

#        if(not (self.valid and other.valid)):
#            new_trace_valid = 0

        new_trace = Trace(new_trace_lst, int(self.valid and other.valid))
                          
        return new_trace
        
    # Trace length
    def __len__(self):
        return len(self.trace)

def best_trace(current_trace, src, dest, env):
   # print("best_trace @X=%d Y=%d" %(src[0], src[1]))
    # current trace : a Trace struct containing cumulative information
    # src, dest : tuple (i,j) representing source/destination coordinates (begins with 0)
    # env : zero-padded (w+2) x (h+2) Map() structure with unknowns marked as 0
    #print("best_trace(%s, %s, %s)" %(current_trace.trace, src, dest))
   
    src_x, src_y = src;
    dest_x, dest_y = dest;

    if(src == dest):
        return Trace([src], 1)

    right = env.elem(src_x+2, src_y+1) and (not (src_x+1, src_y) in current_trace.trace)
    left = env.elem(src_x-1+1, src_y+1) and (not (src_x-1, src_y) in current_trace.trace)
    down = env.elem(src_x+1, src_y+1+1) and (not (src_x, src_y+1) in current_trace.trace)
    up = env.elem(src_x+1, src_y-1+1) and (not (src_x, src_y-1) in current_trace.trace)
    
    trace_r = best_trace(current_trace+Trace([src],1), (src_x+1, src_y), dest, env) if(right) else None
    trace_l = best_trace(current_trace+Trace([src],1), (src_x-1, src_y), dest, env) if(left) else None
    trace_d = best_trace(current_trace+Trace([src],1), (src_x, src_y+1), dest, env) if(down) else None
    trace_u = best_trace(current_trace+Trace([src],1), (src_x, src_y-1), dest, env) if(up) else None

    if(not (right or left or down or up)):
#        print("trapped at %d %d" %(src[0], src[1]))
        return Trace([src], 0)

    traces = [trace_r, trace_l, trace_d, trace_u]
    pathlens = [10000] * 4

    for tr_idx in range(4):
        if(traces[tr_idx]):
            if(traces[tr_idx].valid):
                pathlens[tr_idx] = len(traces[tr_idx])
            
    
    shortest_trace = traces[pathlens.index(min(pathlens))]
    
    return Trace([src],1) + shortest_trace
    
