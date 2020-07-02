from maze_map import Map

INF = 10000

class direction():
    right = 0
    up = 1
    left = 2
    down = 3

class Robot():
    # Pose information
    #   orientation (1,2,3,4)
    ori = 1
    #   abs. coordinate as index 
    x, y = 0, 0

    # The priority of robot(higher priority has larger values)
    # This value must be UNIQUE
    priority = 1

    # The local map is for demonstration result
    # 0 : blocked / 1 : free space(explored) / -1 : unknown
    local_map = []

    explored = []
    trajectory = []

    path_found = 0

    # Project 4, 'best trace' implementation
    # After exit is found, follow_bt is set to 1 and follow the best trace
    follow_bt = 0
    best_trace = []

    # for statistics
    timestamp_now = 0
    arrived = 0
    arrival_timestamp = 0
   
    def __init__(self, priority, maze_x, maze_y, ori=1, x=0, y=0):
        self.ori, self.x, self.y = ori, x, y
        self.local_map = [[-1]*maze_y]*maze_x
        self.priority = priority
        self.trajectory = []
        self.path_found = 0
        self.arrived = 0
        self.arrival_timestamp = 0
        self.best_trace = []
        self.timestamp_now = 0;
        
    
    # After finding solution path, propagate negative potential function back on gpm.
    def propagate_back(self, maze, gpm):
        pass


    # LEFT WALL SCHEME for single
    def explore_left(self, global_maze):
        maze_x, maze_y = global_maze.size_x, global_maze.size_y
        
        while(not (self.x == maze_x - 1 and self.y == maze_y -1)):
            # left side is occupied
            if(self.free_dir(global_maze)[self.ori%4] == 0):
                # turn right until passage appears.
                while(not self.free_dir(global_maze)[(self.ori-1)%4]):
                    self.ori -= 1
                    if(self.ori <= 0):
                        self.ori += 4
                # and move one step forward
                self.propagate_front()
            else:
                self.ori += 1
                if(self.ori > 4):
                    self.ori -= 4
                self.propagate_front()
        self.trajectory.append((maze_x-1, maze_y-1))

            
    # propagate_front : moves to position at watching direction
    def propagate_front(self):
        self.trajectory.append((self.x, self.y))        
        if(self.ori%4 == 0):
            self.y += 1
        elif(self.ori%4 == 1):
            self.x += 1
        elif(self.ori%4 == 2):
            self.y -= 1
        elif(self.ori%4 == 3):
            self.x -= 1

    # propagate(orientation) : move to specified orientation(N,S,E,W) by one step            
    def propagate(self, orientation):
        self.trajectory.append((self.x, self.y))
    
        if(orientation == direction.up):
            self.y -= 1
        elif(orientation == direction.down):
            self.y += 1
        elif(orientation == direction.left):
            self.x -= 1
        elif(orientation == direction.right):
            self.x += 1
       
    # get_potential(global_map, orientation) : get potential value from <global_map> relative to current position
    def get_potential(self, global_map, orientation):
        my_x = self.x + 1
        my_y = self.y + 1

        if(orientation == direction.up):
            return global_map.elem(my_x, my_y-1)
        elif(orientation == direction.down):
            return global_map.elem(my_x, my_y+1)
        elif(orientation == direction.left):
            return global_map.elem(my_x-1, my_y)
        elif(orientation == direction.right):
            return global_map.elem(my_x+1, my_y)
    
    def free_dir(self, global_maze):
        l, r, u, d = 0, 0, 0, 0
        maze_x, maze_y = global_maze.size_x, global_maze.size_y

        if(self.x > 0):
            l = global_maze.elem(self.x-1, self.y)
            if((self.x-1, self.y) in self.explored):
                l = 0
        if(self.y > 0):
            u = global_maze.elem(self.x, self.y-1)
            if((self.x, self.y-1) in self.explored):
                u = 0
        if(self.x < maze_x - 1):
            r = global_maze.elem(self.x+1, self.y) # [maze_x * self.y + self.x + 1]
            if((self.x+1, self.y) in self.explored):
                r = 0
        if(self.y < maze_y - 1):
            d = global_maze.elem(self.x, self.y+1) #[maze_x * (self.y+1) + self.x]
            if((self.x, self.y+1) in self.explored):
                d = 0
            
        return [r, u, l, d]

    # at robot's location, list free directions for NSEW
    def free_dir_abs(self, global_maze):
        l, r, u, d = 0, 0, 0, 0

        maze_x, maze_y = global_maze.size_x, global_maze.size_y

        if(self.x > 0):
            l = global_maze.elem(self.x-1, self.y)
        if(self.y > 0):
            u = global_maze.elem(self.x, self.y-1)
        if(self.x < maze_x - 1):
            r = global_maze.elem(self.x+1, self.y) # [maze_x * self.y + self.x + 1]
        if(self.y < maze_y - 1):
            d = global_maze.elem(self.x, self.y+1) #[maze_x * (self.y+1) + self.x]
        
        return [r, u, l, d]


    def trajectory_map(self, global_maze):
        # new_map = Map(global_maze.data, global_maze.size_x, global_maze.size_y)
        new_map_data = list()
        
        for elem in global_maze.data:
            new_map_data.append(elem)

        new_map = Map(new_map_data, global_maze.size_x, global_maze.size_y)

        for history in self.trajectory:
            new_map.set(history[0], history[1], self.priority)


        return new_map

    # global map data structure
    # An array of length [(m+2)x(n+2)] representing (m+2)x(n+2) matrix
    # Take map, m, n as arguments


    # broadcast : broadcasts current cell's modified potential value
    def broadcast(self, maze, gpm):
        if(not self.path_found):
            # gpm : global potential map
            # maze : actual maze structure <const>        
    
            # free directions (R, U, L, D)
            free_dirs = self.free_dir_abs(maze)
    
            # index change due to sentinels
            gpm_x, gpm_y = self.x+1, self.y+1
    
            if(not free_dirs[2]):
                gpm.set(gpm_x-1, gpm_y, INF)    
            if(not free_dirs[0]):
                gpm.set(gpm_x+1, gpm_y, INF)    
            if(not free_dirs[1]):
                gpm.set(gpm_x, gpm_y-1, INF)    
            if(not free_dirs[3]):
                gpm.set(gpm_x, gpm_y+1, INF)    
    
            potential_dirs = [gpm.elem(gpm_x+1,gpm_y), gpm.elem(gpm_x-1,gpm_y), gpm.elem(gpm_x,gpm_y-1), gpm.elem(gpm_x,gpm_y+1)]
            
            if(potential_dirs.count(INF) == 3):
                gpm.set(gpm_x, gpm_y, INF)
            else:
                gpm.set(gpm_x, gpm_y, gpm.elem(gpm_x, gpm_y) + 1)

        else:
            return

    # move : move to cell where potential is minimum.
    # raises errror if there's no way to go
    def move(self,maze, gpm):
        if(self.arrived):
            return

        if(self.follow_bt):
            self.trajectory.append((self.x, self.y))
            self.x, self.y = self.best_trace.pop(0)
            if(self.x == gpm.size_x-3 and self.y == gpm.size_y-3):
                self.arrived = 1
            return
        
        if(self.x == gpm.size_x-3 and self.y == gpm.size_y-3):
            # print("Robot %s arrived at position %d %d" %(self.priority, self.x,self.y))
            self.trajectory.append((self.x, self.y))
            self.path_found = 1
            self.arrived = 1
            return
        
        self.trajectory.append((self.x, self.y))
        
        Uu, Ud, Ul, Ur = self.get_potential(gpm, direction.up), self.get_potential(gpm, direction.down), self.get_potential(gpm, direction.left), self.get_potential(gpm, direction.right)

        pot_4dir = [Uu, Ud, Ul, Ur]

        #print("ROBOT#%d : %s" %(self.priority, pot_4dir))
        min_pot = min(pot_4dir)

        if(min_pot == INF):
            raise ValueError("U values are infinite for 4 directions")
        else:
            #self.ori is initialized value 1
            #choose priority by previous heading
            #if previous heading is up
            if(self.ori==direction.up):
                if(min_pot==Uu):
                    self.y-=1
                    self.ori=direction.up
                elif(min_pot==Ul):
                    self.x-=1
                    self.ori=direction.left
                elif(min_pot==Ud):
                    self.y+=1
                    self.ori=direction.down
                elif(min_pot==Ur):
                    self.x+=1
                    self.ori=direction.right
            #if previous heading is right        
            elif(self.ori==direction.right):
                if(min_pot==Ur):
                    self.x+=1
                    self.ori=direction.right
                elif(min_pot==Uu):
                    self.y-=1
                    self.ori=direction.up
                elif(min_pot==Ul):
                    self.x-=1
                    self.ori=direction.left
                elif(min_pot==Ud):
                    self.y+=1
                    self.ori=direction.down
            #if previous heading is left 
            elif(self.ori==direction.left):
                if(min_pot==Ul):
                    self.x-=1
                    self.ori=direction.left
                elif(min_pot==Ud):
                    self.y+=1
                    self.ori=direction.down
                elif(min_pot==Ur):
                    self.x+=1
                    self.ori=direction.right
                elif(min_pot==Uu):
                    self.y-=1
                    self.ori=direction.up
            #if previous heading is down
            elif(self.ori==direction.down):
                if(min_pot==Ud):
                    self.y+=1
                    self.ori=direction.down
                elif(min_pot==Ur):
                    self.x+=1
                    self.ori=direction.right
                elif(min_pot==Uu):
                    self.y-=1
                    self.ori=direction.up
                elif(min_pot==Ul):
                    self.x-=1
                    self.ori=direction.left
                
                    
            



        if(not self.path_found):
            gpm.set(self.x+1, self.y+1, gpm.elem(self.x+1, self.y+1) + 1)
        
