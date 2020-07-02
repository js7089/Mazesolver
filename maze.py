from PIL import Image, ImageDraw
from random import randint

width, height = 400, 400
RAND_MIN, RAND_MAX = 0, 1000

im = Image.new('RGBA', (width, height), (0, 0, 0, 0))

def draw_rectangle(canvas, i, j):
    drawer = ImageDraw.Draw(canvas)
    drawer.rectangle([(10*i, 10*j), (10*i + 10, 10*j + 10)], fill="#0aaaaa", outline = None)

def generate_matrix(xsize, ysize):
    A = [[0]*ysize]*xsize

    for i in range(xsize):
        for j in range(ysize):
            A[i][j] = randint(RAND_MIN, RAND_MAX-1)

    return A

def generate_maze(matrix, xsize, ysize):
    pos_x, pos_y = 0, ysize-1

    B = [[0]*ysize]*xsize

    B[pos_x][pos_y] = 1
    matrix[pos_x][pos_y] = RAND_MAX
    print("matrix[%d][%d] = RAND_MAX" %(pos_x, pos_y))

    while(next_pos_to_go(matrix, pos_x, pos_y, xsize, ysize) != None):
        pos_x, pos_y = next_pos_to_go(matrix, pos_x, pos_y, xsize, ysize)
        print([pos_x, pos_y])
        B[pos_x][pos_y] = 1
        
        matrix[pos_x][pos_y] = RAND_MAX
        if(pos_x < xsize-1):
            matrix[pos_x+1][pos_y] = RAND_MAX
        if(pos_x > 0):    
            matrix[pos_x-1][pos_y] = RAND_MAX
        if(pos_y < ysize-1):    
            matrix[pos_x][pos_y+1] = RAND_MAX
        if(pos_y > 0):
            matrix[pos_x][pos_y-1] = RAND_MAX



        # print("matrix[%d][%d] = RAND_MAX" %(pos_x, pos_y))
    print(B)
    return B


def next_pos_to_go(matrix, pos_x, pos_y, xsize, ysize):
    w_up, w_down, w_left, w_right = RAND_MAX, RAND_MAX, RAND_MAX, RAND_MAX

    if(pos_x > 0):
        w_left = matrix[pos_x-1][pos_y]
    if(pos_x < xsize-1):
        w_right = matrix[pos_x+1][pos_y]
    if(pos_y > 0):
        w_up = matrix[pos_x][pos_y-1]
    if(pos_y < ysize-1):
        w_down = matrix[pos_x][pos_y+1]

    min_weight = min([w_up, w_down, w_left, w_right])

    if(min_weight >= RAND_MAX):
        return None

    if(min_weight == w_up):
        return (pos_x, pos_y-1)
    elif(min_weight == w_down):
        return (pos_x, pos_y+1)
    elif(min_weight == w_left):
        return (pos_x-1, pos_y)
    elif(min_weight == w_right):
        return (pos_x+1, pos_y)
    else:
        return None
    

A = generate_matrix(10,10)
generate_maze(A,10,10)

        
