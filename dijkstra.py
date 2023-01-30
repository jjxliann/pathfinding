import pygame
import math
from queue import PriorityQueue

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption("Pathfinding visualizer")

col = 50
rows = 50
boxWidth = WIDTH // col
boxHeight = WIDTH // rows

arr = []
q = []

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (80, 80, 80)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Spot:
    def __init__(self,i,j):
        self.x = i
        self.y = j
        self.color = WHITE
        self.start = False
        self.wall = False
        self.queued = False
        self.visited = False
        self.neighbors = []

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color ==GREEN

    def is_wall(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def make_start(self):
        self.color = ORANGE

    def reset(self):
        self.color = WHITE

    def make_closed(self):
        self.color = RED
    
    def make_open(self):
        self.color = GREEN
    
    def make_wall(self):
        self.color = BLACK
    
    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE
    
    def draw(self,win):
        pygame.draw.rect(win,self.color,(self.x, self.y, self.width, self.width))

    def setNeighbors(self):
        if  self.row < self.total_rows -1 : #DOWN
                self.neighbors.append(arr[self.row + 1][self.col])

        if  self.row > 0 : #UP
                self.neighbors.append(arr[self.row - 1][self.col])

        if  self.col < self.total_rows -1: #R
                self.neighbors.append(arr[self.row][self.col + 1])

        if  self.col > 0: #L
                self.neighbors.append(arr[self.row][self.col -1])

    for i in range(col):
        for j in range(rows):
            arr[i][j].setNeighbors()

    start_box = arr[0][0]
    start_box.start = True
    start_box.visited = True
    

    


def h(p1, p2):
    x1,y1 = p1
    x2,y2 = p2
    return abs(x1 -x2) + abs(y1 - y2)

def reconstructPath(came_from, curr, draw):
    while curr in came_from:
        curr = came_from[curr]
        curr.make_path()
        draw()




def create_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i,j,gap,rows)
            grid[i].append(spot)

    return grid

def drawGrid(win,rows,width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY,(0, i * gap),(width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY,(j* gap, 0),( j * gap, width))

def draw(win, grid ,rows, width):
    win.fill(WHITE)

    for row in grid:
        for spot in row:
            spot.draw(win)
    drawGrid(win,rows,width)
    pygame.display.update()

def get_click_pos(pos,rows,width):
    gap = width // rows
    y,x = pos

    row = y // gap
    col =  x // gap

    return row, col

def  main(win,width):
    ROWS = 50
    grid = create_grid(ROWS, width)

    start = None
    end = None

    run = True
    while run:
        draw(win,grid,ROWS,width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
          

            if pygame.mouse.get_pressed()[0]: #left
                pos = pygame.mouse.get_pos()
                row,col = get_click_pos(pos, ROWS, width)
                spot = grid[row][col]
                if not start and spot != end:
                    start = spot
                    start.make_start()

                elif not end and spot != start:
                    end = spot
                    end.make_end()
                
                elif spot != end and spot != start:
                    spot.make_wall()
            
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row,col = get_click_pos(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                if spot  == start:
                    start = None
                elif spot == end:
                    end = None
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    
                    algorithm(lambda: draw(win,grid, ROWS, width), grid, start, end)
                
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = create_grid(ROWS,width)


    pygame.quit()
    return main(WIN,WIDTH)