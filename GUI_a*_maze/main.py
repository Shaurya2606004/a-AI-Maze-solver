#import main
import pygame
import numpy as np
import heapq 

start=(2,5)
goal=(5,16)

def heuristics(a,b):
  return np.sqrt((b[0]-a[0])**2 + (b[1]-a[1])**2)


def astar(array,start,end):
  directions=[(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]
  closed_list=set()
  came_from={}
  gscore={start:0}                        # dictionary key : value pairs
  fscore={start:heuristics(start,goal)}  # a dictionary 

  openlist=[] # FRONTIER
  heapq.heappush(openlist,(fscore[start],start)) #priority queue, 
  #in frontier priority by fscore and followed by identir of that fscore

  while openlist:
    current=heapq.heappop(openlist)[1] #fscore wise at index 1 (x,y) coordinate

    if current==goal:
      path_data=[]  # contain entire path 
      while current in came_from:
        path_data.append(current)
        current=came_from[current]
      return path_data

    closed_list.add(current)
    
    for i,j in directions:
      direction= current[0] +i , current[1]+j
      temp_gscore= gscore[current]+heuristics(current,direction)
      if 0<= direction[0]<len(array[0]):  #corner case to consider boundary
        if 0<=direction[1]<len(array[1]):
          if array[direction[0]][direction[1]] ==1 : #obstacle
            continue

        else:
            #column wall
          continue
      else:
        # row wall
        continue
      if direction in closed_list and temp_gscore >= gscore.get(direction,0):
        continue
      
      if temp_gscore <gscore.get(direction,0) or direction not in [i[1] for i in openlist]:
        came_from[direction]=current
        gscore[direction]=temp_gscore
        fscore[direction]= temp_gscore+heuristics(direction,goal)
        heapq.heappush(openlist,(fscore[direction],direction))
  return False #incase no path found


def draw_ans(route,grid):
    pygame.init()
    route.pop()
    # Set the HEIGHT and WIDTH of the screen
    WINDOW_SIZE = [520, 520]
    screen = pygame.display.set_mode(WINDOW_SIZE)

    # Set title of screen
    pygame.display.set_caption("AI MAZE SOLVER")

    # Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    for i,j in route:
        grid[i][j]=3
    while not done:
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True
        for row in range(20):
            for column in range(20):
                color = WHITE
                if grid[row][column] == 1:
                    color = BLACK
                if grid[row][column]==2:
                    color=RED
                if grid[row][column]==3:
                    color=GREEN
                pygame.draw.rect(screen,
                                color,
                                [(MARGIN + WIDTH) * column + MARGIN,
                                (MARGIN + HEIGHT) * row + MARGIN,
                                WIDTH,
                                HEIGHT])

        # Limit to 60 frames per second
        clock.tick(60)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

WIDTH = 20
HEIGHT =20

MARGIN = 8

grid = []
for row in range(20):
    
    grid.append([])
    for column in range(20):
        grid[row].append(0)  # Append a cell

print(grid)
grid[2][5] = 2
grid[5][16]=2

pygame.init()

WINDOW_SIZE = [540, 540]
screen = pygame.display.set_mode(WINDOW_SIZE)

pygame.display.set_caption("AI MAZE SOLVER")

done = False

clock = pygame.time.Clock()

while not done:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:  #  user close
            done=True  # Flag that we are done so we exit this loop
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            column = pos[0] // (WIDTH + MARGIN)
            row = pos[1] // (HEIGHT + MARGIN)
            grid[row][column] = 1
            #print("Click ", pos, "Grid coordinates: ", row, column)

    # Set the screen background
    screen.fill(BLACK)

    # Draw the grid
    for row in range(20):
        for column in range(20):
            color = WHITE
            if grid[row][column] == 1:
                color = BLACK
            if grid[row][column]==2:
                color=RED
            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])

    clock.tick(60)
    pygame.display.flip()


route=astar(grid,start,goal)

if(route!=False):
    route=route[::-1] #reverse
    draw_ans(route, grid)
    route= route+[start]
    print(route)
else:
    print("NO PATH FOUND")
pygame.quit()
