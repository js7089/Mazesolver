from PIL import Image, ImageDraw, ImageFont
from random import randint, sample
from maze_runner import Robot
from maze_map import Map, Trace, best_trace

DEBUG = 0

# size of each rectangular cell
cell_size = 20

# iterations
iter_max = 600

INF = 10000

def draw_robot(canvas, j, i, color):
    drawer = ImageDraw.Draw(canvas)
    drawer.ellipse([(cell_size*(i+0.25), cell_size*(j+0.25)), (cell_size*(i+0.75), cell_size*(j+0.75))], fill=color, outline = None)
     
def draw_rectangle(canvas, j, i):
    drawer = ImageDraw.Draw(canvas)
    drawer.rectangle([(cell_size*i, cell_size*j), (cell_size*(i+1), cell_size*(j+1))], fill="#000000", outline = None)

def draw_blank(canvas, j, i):
    drawer = ImageDraw.Draw(canvas)
    drawer.rectangle([(cell_size*i, cell_size*j), (cell_size*(i+1), cell_size*(j+1))], fill="#eaeaea", outline = None)

def draw_unknown(canvas, j, i):
    drawer = ImageDraw.Draw(canvas)
    drawer.rectangle([(cell_size*i, cell_size*j), (cell_size*(i+1), cell_size*(j+1))], fill="#444444", outline = None)


def draw_trajectory(canvas, j, i, color):
    drawer = ImageDraw.Draw(canvas)
    drawer.rectangle([(cell_size*i, cell_size*j), (cell_size*(i+1), cell_size*(j+1))], fill=color, outline = None)


def generate_matrix(xsize, ysize):
    if(DEBUG):
        print("generate_matrix(%d,%d)" %(xsize, ysize), end=" ")
        

    A = [1]*xsize*ysize

    if(xsize <= 2 or ysize <= 2):
        if(xsize == 1 or ysize == 1):
            return A

        if(xsize == 2 and ysize >2):
            pivot_x, pivot_y = randint(0, 1), randint(1, ysize-2)

            holes = [ (1-pivot_x, pivot_y),
                  (pivot_x, randint(0, pivot_y-1)),
                  (pivot_x, randint(pivot_y+1, ysize-1)) ]

            result = concat(generate_matrix(pivot_x, pivot_y),
                      generate_matrix(xsize - pivot_x - 1, pivot_y),
                      generate_matrix(pivot_x, ysize - pivot_y - 1),
                      generate_matrix(xsize - pivot_x - 1, ysize - pivot_y - 1),
                      xsize, ysize, pivot_x, pivot_y)

            for points in holes:
                result[points[0] + xsize*points[1]] = 1

        elif(xsize > 2 and ysize == 2):
            pivot_x, pivot_y = randint(1, xsize-2), randint(0, 1)

            holes = [ (randint(0, pivot_x-1), pivot_y),
                      (randint(pivot_x+1, xsize-1), pivot_y),
                      (pivot_x, (1-pivot_y)) ]

            result = concat(generate_matrix(pivot_x, pivot_y),
                      generate_matrix(xsize - pivot_x - 1, pivot_y),
                      generate_matrix(pivot_x, ysize - pivot_y - 1),
                      generate_matrix(xsize - pivot_x - 1, ysize - pivot_y - 1),
                      xsize, ysize, pivot_x, pivot_y)

            for points in holes:
                result[points[0] + xsize*points[1]] = 1

        
        return A
    else:
        pivot_x, pivot_y = randint(1, xsize-2), randint(1, ysize-2)
        # pivot_x, pivot_y = int(0.5*xsize), int(0.5*ysize)
        
        holes = [ (randint(0, pivot_x-1), pivot_y),
                  (randint(pivot_x+1, xsize-1), pivot_y),
                  (pivot_x, randint(0, pivot_y-1)),
                  (pivot_x, randint(pivot_y+1, ysize-1)) ]

        holes_chosen = sample(holes, 3)

        result = concat(generate_matrix(pivot_x, pivot_y),
                      generate_matrix(xsize - pivot_x - 1, pivot_y),
                      generate_matrix(pivot_x, ysize - pivot_y - 1),
                      generate_matrix(xsize - pivot_x - 1, ysize - pivot_y - 1),
                      xsize, ysize, pivot_x, pivot_y)

        for points in holes_chosen:
            result[points[0] + xsize*points[1]] = 1



        for i in range(1,xsize-1):
            for j in range(1,ysize-1):
                if(illegal(result, i, j, xsize, ysize)):
                    result[i + xsize*j] = 1

        return result

def concat(A1, A2, A3, A4, w, h, piv_x, piv_y):
    result = [0]*w*h
    for rows in range(piv_y):
        for cols in range(piv_x):
            result[w*rows + cols] = A1[piv_x*rows + cols]
        for cols in range(piv_x + 1, w):
            result[w*rows + cols] = A2[(w-piv_x-1)*rows + (cols-(piv_x+1))]

    for rows in range(piv_y+1, h):
        for cols in range(piv_x):
            result[w*rows + cols] = A3[piv_x*(rows-(piv_y+1)) + cols]
        for cols in range(piv_x + 1, w):
            result[w*rows + cols] = A4[(w-piv_x-1)*(rows-(piv_y+1)) + (cols-(piv_x+1))]
    
    return result
                  
def illegal(matrix, i, j, w, h):
    up = (not matrix[(i-1) + (j-1)*w]) & (not matrix[(i+1) + (j-1)*w]) & matrix[(i) + (j-1)*w]
    down = (not matrix[(i-1) + (j+1)*w]) & (not matrix[(i+1) + (j+1)*w]) & matrix[(i) + (j+1)*w]
    left = (not matrix[(i-1) + (j-1)*w]) & (not matrix[(i-1) + (j+1)*w]) & matrix[(i-1) + (j)*w]
    right = (not matrix[(i+1) + (j-1)*w]) & (not matrix[(i+1) + (j+1)*w]) & matrix[(i+1) + (j)*w]

    return up | down | left | right 

def free_cell(matrix, i, j, w, h):
    pass

def test_concat():        
    px, py = 1, 2
    w, h = 10, 10

    A = [1]*px*py
    B = [2]*(w-px-1)*py
    C = [3]*px*(h-py-1)
    D = [4]*(w-px-1)*(h-py-1)

    result = concat(A,B,C,D,w,h,px,py)

def show_matrix(A, xsize, ysize):
    # A = generate_matrix(xsize, ysize)

    for i in range(ysize):
        for j in range(xsize):
            print("%s" %("▒" if(A[i*xsize + j]) else "■"),end="")
        print("")
        
def maze(matrix,im, xsize, ysize):
    for i in range(ysize):
        for j in range(xsize):
            if(matrix[i*xsize + j] == 0):
                draw_rectangle(im, i, j)
            elif(matrix[i*xsize + j] == 1):
                draw_blank(im,i,j)
            else:
                mark_pivot(im,i,j)
                
    return im

def draw_matrix(maze_map,maze_x,maze_y):
    im = Image.new('RGBA', (cell_size*maze_map.size_x, cell_size*maze_map.size_y),(255, 0, 0, 1))
    draw = ImageDraw.Draw(im)
    for i in range(maze_map.size_y):
        for j in range(maze_map.size_x):
            if(maze_map.elem(j,i) == 0):
                draw_rectangle(im,i,j)
            elif(maze_map.elem(j,i) == 1):
                draw_blank(im,i,j)
            #elif(maze_map.elem(j,i) >= 2):
            #    draw_trajectory(im,i,j,"yellow")

    borderwidth = 1
    
    draw.line([(0,0), (0,-1+maze_y*cell_size)], width=2, fill="black")
    draw.line([(-1+maze_x*cell_size,-1+maze_y*cell_size), (0,-1+maze_y*cell_size)], width=2, fill="black")
    draw.line([(-1+maze_x*cell_size,-1+maze_y*cell_size), (-1+maze_x*cell_size,0)], width=2, fill="black")
    draw.line([(-1+maze_x*cell_size,0), (0,0)], width=2, fill="black")

    del draw

    return im

    
def simulate(maze_x, maze_y, N_robots, generate_image,aux):
    # Graphical effects
    colors = []
    for robots in range(N_robots):
        r = randint(0,256)
        g = randint(0,256)
        b = randint(0,256)
        colors.append(("#" + "{0:0{1}x}".format(r*256*256 + g*256 + b,6))[0:7])

    # Map generation
    im = Image.new('RGBA', (cell_size*maze_x, cell_size*maze_y),(255, 0, 0, 1))

    A = generate_matrix(maze_x, maze_y)

    # Map() data structure for generated array A
    maze_map = Map(A, maze_x, maze_y)

    # Map() augmented with sentinel inf and 0 of width 1
    B = [INF] * (maze_x+2) * (maze_y+2)
    C = [0] * (maze_x + 2) * (maze_y + 2)
    
    for y_idx in range(maze_y):
        for x_idx in range(maze_x):
            B[(maze_x+2)*(y_idx+1) + (x_idx+1)] = 0 #A[maze_x*y_idx + x_idx]
            C[(maze_x+2)*(y_idx+1) + (x_idx+1)] = A[maze_x*y_idx + x_idx]
            
    potential_map = Map(B, maze_x+2, maze_y+2)
    env_trace = Map(C, maze_x+2, maze_y+2)
    
    # Union of all coordinates (x,y) explored by robots
    explored_global = []
    
    # <Graphics> draw original maze map structure
    draw = ImageDraw.Draw(im)
    borderwidth = 1
    
    im = maze(A, im, maze_x, maze_y)

    # Marking start/endpoint
    draw.rectangle([(0,0), (cell_size, cell_size)], fill="red", outline = None)
    draw.rectangle([(cell_size*(maze_x-1),cell_size*(maze_y-1)), (cell_size*(maze_x), cell_size*(maze_y))], fill="blue", outline = None)

    # Save original maze structure
    if(aux == 1):
        im.save("maze_" + str(maze_x) + "by" + str(maze_y) + ".png")

    
    # Robot 'object' declaration
    robots = list()
    glob_trajectory = []

    # Graphics
    fnt = ImageFont.load_default()
    im_sequence = []

    # Statistics
    result_multi_iter = []
    result_sgl_iter = 0
    
    for i in range(N_robots):
        robots.append(Robot(i, maze_x, maze_y, 1, 0, 0))

    for iterations in range(iter_max):
        maze_graphic = draw_matrix(maze_map,maze_x,maze_y)

        T_local_ptr = set()        
        for r_t in robots:
            T_local_ptr = T_local_ptr.union(r_t.trajectory)
            
        glob_trajectory = T_local_ptr
        glob_unknown = set()

        for idxY in range(maze_y):
            for idxX in range(maze_x):
                glob_unknown.add((idxX,idxY))

        for entry in glob_trajectory:
            if((entry[0], entry[1]) in glob_unknown):
                glob_unknown.remove((entry[0],entry[1]))
            if((entry[0]+1, entry[1]) in glob_unknown):
                glob_unknown.remove((entry[0]+1,entry[1]))
            if((entry[0], entry[1]+1) in glob_unknown):
                glob_unknown.remove((entry[0],entry[1]+1))
            if((entry[0], entry[1]-1) in glob_unknown):
                glob_unknown.remove((entry[0],entry[1]-1))
            if((entry[0]-1, entry[1]) in glob_unknown):
                glob_unknown.remove((entry[0]-1,entry[1]))
                                       

        for unexplored in glob_unknown:
            draw_unknown(maze_graphic,unexplored[1],unexplored[0])

            
        for r_ptr in robots:
            draw_robot(maze_graphic, r_ptr.y, r_ptr.x, colors[r_ptr.priority])

        im_sequence.append(maze_graphic)
        d = ImageDraw.Draw(maze_graphic)
        
        d.text((0,0), text=("iter=" + str(iterations)), font=fnt, fill=(255,255,0,200))
        
        end_switch = 1

        for r_ptr in robots:
            end_switch &= r_ptr.arrived

        if(end_switch):
            #print("After %d iterations, all %d robots has arrived exit at (%d, %d)" %(iterations, N_robots, maze_x-1, maze_y-1))
            for r_ptr in robots:
                # halts one frame when calling best_trace()
                result_multi_iter.append(len(r_ptr.trajectory)-1)
            break
        
        for r_s in robots:
            r_s.broadcast(maze_map, potential_map)
            r_s.move(maze_map, potential_map)
            
            if(r_s.path_found):
                T_local = set()
                glob_unknown_final = set()

                for r_t in robots:
                    r_t.path_found = 1
                    T_local = T_local.union(r_t.trajectory)

                for idxY in range(maze_y):
                    for idxX in range(maze_x):
                        glob_unknown_final.add((idxX,idxY))

                for entry in T_local:
                    if((entry[0], entry[1]) in glob_unknown_final):
                        glob_unknown_final.remove((entry[0],entry[1]))
                    if((entry[0]+1, entry[1]) in glob_unknown_final):
                        glob_unknown_final.remove((entry[0]+1,entry[1]))
                    if((entry[0], entry[1]+1) in glob_unknown_final):
                        glob_unknown_final.remove((entry[0],entry[1]+1))
                    if((entry[0], entry[1]-1) in glob_unknown_final):
                        glob_unknown_final.remove((entry[0],entry[1]-1))
                    if((entry[0]-1, entry[1]) in glob_unknown_final):
                        glob_unknown_final.remove((entry[0]-1,entry[1]))

                for entry in glob_unknown_final:
                    env_trace.set(entry[0]+1, entry[1]+1, 0)

                for r_t in robots:
                    if(not r_t.follow_bt):
                        r_t_BT = best_trace(Trace([(r_t.x, r_t.y)]), (r_t.x,r_t.y), (maze_x-1, maze_y-1), env_trace)
                        r_t.best_trace = r_t_BT.trace
                        r_t.follow_bt = 1
                    
    if(generate_image):     
        im.save("multi_" + str(maze_x) + "by" + str(maze_y) + "_result_" + str(N_robots) + "agents_" + str(aux) +".gif", save_all=True, append_images = im_sequence, loop=0)

        
    # Comparing with single robot

    a = Robot(200, maze_x, maze_y)
    a.explore_left(maze_map)

    jm_sequence = []
    for iterations_single in range(len(a.trajectory)):
        maze_graphic = draw_matrix(maze_map,maze_x,maze_y)

        draw_robot(maze_graphic, a.trajectory[iterations_single][1], a.trajectory[iterations_single][0], colors[0])
        
        jm_sequence.append(maze_graphic)
        d = ImageDraw.Draw(maze_graphic)
        
        d.text((0,0), text=("iter=" + str(iterations_single)), font=fnt, fill=(255,255,0,200))

    #print("After %d iterations, a single robot has arrived exit at (%d, %d)" %(len(a.trajectory), maze_x-1, maze_y-1))

    if(generate_image):
        im.save("sgl_" + str(maze_x) + "by" + str(maze_y) + "_result" + str(aux) + ".gif", save_all=True, append_images = jm_sequence, loop=0)

    
    result_sgl_iter = len(a.trajectory)
    
    return (result_multi_iter, result_sgl_iter)


def adjacant(traj_elem, this_elem):
    return (abs(traj_elem[0]-this_elem[0]) == 1) and (traj_elem[1]==this_elem[1]) or (abs(traj_elem[1]-this_elem[1]) == 1) and (traj_elem[0]==this_elem[0])
                      
    
def draw_local_map(canvas, maze_map, trajectory, priority):
    for ydx in range(maze_map.size_y):
        for xdx in range(maze_map.size_x):
            if(not (xdx,ydx) in trajectory):
                bool_adj = 0
                for elem in trajectory:
                    bool_adj |= adjacant((xdx,ydx), elem)
                if(not bool_adj):
                    draw_unknown(canvas, ydx, xdx)

    d = ImageDraw.Draw(canvas)
    fnt = ImageFont.load_default()
    d.text((0,0), text=("Map" + str(priority)), font=int, fill=(255,255,0,200))

if __name__=='__main__':
    SIMULATION_SIZE = 20
    sim_x=15
    sim_y=10
    nagents=8
    gen_img = 1

    print("--- Maze simulation ---")
    print(" Maze size : [%d x %d]" %(sim_x, sim_y))
    print(" Using %d Agents " %(nagents))
    print(" For %d testcases" %(SIMULATION_SIZE))
    print("-----------------------")

    print("Test\t***\tMulti\t***\tSingle\ncase\tmean\tmin\tmax\t\tRatio")

    ma_sum = 0
    mmin_sum = 0
    mmax_sum = 0
    sgl_sum = 0
    rat_sum = 0.0
    
    for i in range(SIMULATION_SIZE):
        multi, sgl = simulate(sim_x,sim_y,nagents,gen_img,i+1)
        multi_avg = sum(multi)/len(multi)
        multi_max = max(multi)
        multi_min = min(multi)

        ma_sum += multi_avg
        mmin_sum += multi_min
        mmax_sum += multi_max
        sgl_sum += sgl
        rat_sum += 1/sgl*multi_avg
        
        print("%d\t%d\t%d\t%d\t%d\t%.2f\t" %(i+1,multi_avg, multi_min, multi_max, sgl, 1/sgl*multi_avg))


    print("Avg.\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t" %(ma_sum/SIMULATION_SIZE, mmin_sum/SIMULATION_SIZE, mmax_sum/SIMULATION_SIZE, sgl_sum/SIMULATION_SIZE, rat_sum/SIMULATION_SIZE))
    

