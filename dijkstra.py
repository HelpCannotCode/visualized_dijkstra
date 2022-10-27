# a* pathfinding algorithm "visual" written by aaaron 
# this code makes a visual of the a* algorithm
import math, pygame
from queue import PriorityQueue


WIDTH = 400
WINDOW = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption("algorithm")

#color codes 
RED = (222, 10, 0)
WHITE = (255, 255, 255)
BLUE = (2, 20, 80)
GREEN = (12, 182, 17)
ORANGE = (243, 156, 18 )
PINK = (241, 78, 214 )
BLACK = (0, 0, 0)

#class for squares
class Squares:
  def __init__(self,row,col,width,total_rows):
    self.row = row
    self.col = col
    self.x = row * width
    self.y = col * width
    self.neighbours = []
    self.width = width
    self.total_rows = total_rows
    self.color = WHITE

  def get_pos(self):
    return self.row, self.col
  
  #colour defines what square is path,start, end,etc.
  def checked(self):
    return self.color == RED

  def barrier(self):
    return self.color == BLACK

  def start_square(self):
    return self.color == ORANGE

  def end_square(self):
    return self.color == BLUE

  def unchecked(self):
    return self.color == GREEN

  # these set each square to start, end, etc
  def reset(self):
    self.color = WHITE

  def make_start_square(self):
    self.color = ORANGE

  def make_end_square(self):
    self.color = BLUE

  def make_unchecked(self):
    self.color = RED

  def make_checked(self):
    self.color = GREEN

  def make_barrier(self):
    self.color = BLACK

  def make_path(self):
    self.color = PINK

  def draw(self, WINDOW): #draw square
    pygame.draw.rect(WINDOW, self.color,(self.x,self.y,self.width,self.width))

  def update_neighbours(self, grid):# gets neigbouring squares
    self.neighbours = []
    # rows go up to down cols go left to right
    #down square
    # if row less than max and no barrier below
    if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].barrier():
       self.neighbours.append(grid[self.row + 1][self.col])

    # right square
    if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].barrier():
       self.neighbours.append(grid[self.row][self.col+1])
       
    #up square
    if self.row > 0 and not grid[self.row - 1][self.col].barrier():
       self.neighbours.append(grid[self.row - 1][self.col])

    # left square
    if self.col > 0  and not grid[self.row ][self.col - 1].barrier():
       self.neighbours.append(grid[self.row][self.col - 1])



def h(point1,point2):
  x1, y1 = point1
  x2, y2 = point2
  return abs(x1-x2) + abs(y1-y2)

#draws the shortest path
def draw_path(came_from,current,draw):
  while current in came_from:
    current = came_from[current]
    current.make_path()
    draw()

def algorithm(draw,grid,start,end):
  count = 0 # count prioritizes the earlier in case of equal f and g scores
  open_set = PriorityQueue()#the queue of where we should go
  open_set.put((0,count,start))
  came_from = {}#node came from
  # g score first travel score
  # the start costs nothing to move to
  g_score = {Squares: float("inf")for row in grid for Squares in row }
  g_score[start] = 0
  # f score distance away from end/goal
  f_score = {Squares: float("inf")for row in grid for Squares in row}#"inf" = infinity
  f_score[start] = h(start.get_pos(),end.get_pos())

  open_set_hash = {start} # keeps track of squares in set

  while not open_set.empty():
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
    
    current = open_set.get()[2] # get the square/node
    open_set_hash.remove(current)

    if current == end:
      draw_path(came_from,end,draw)
      end.make_end_square()
      return True
    
    for neighbour in current.neighbours:
      temp_g_score = g_score[current] + 1
      
      # determine neighbour's g and f score 
      if temp_g_score < g_score[neighbour]:
        came_from[neighbour] = current
        g_score[neighbour] = temp_g_score
        f_score[neighbour] = temp_g_score + h(neighbour.get_pos(), end.get_pos())
        #for all new squares scores placing them in the set
        if neighbour not in open_set_hash:
          count += 1
          open_set.put((f_score[neighbour],count,neighbour))
          open_set_hash.add(neighbour)
          neighbour.make_unchecked()
    draw()  

    if current != start:
      current.make_checked() 
    

  return False

# makes the grid of squares 
def make_grid(rows,width):
  grid = []#list of rows
  gap = width // rows
  for i in range(rows):
    grid.append([])
    for j in range(rows):
      square = Squares(i,j,gap,rows)
      grid[i].append(square)
  return grid

#draw gridlines
def draw_grid(WINDOW, rows, width):
  
  gap = width // rows
  for i in range(rows):
    pygame.draw.line(WINDOW,BLACK, (0,i*gap),(width, i*gap))
    for j in range(rows):
      pygame.draw.line(WINDOW,BLACK, (j*gap,0),(j*gap,width))

 #draw the window     
def draw(WINDOW,grid,rows,width):
  WINDOW.fill(WHITE)

  for row in grid:
    for Squares in row:
      Squares.draw(WINDOW)
  

  draw_grid(WINDOW, rows, width)
  pygame.display.update()

#finds the mouse's square
def get_clicked_pos(pos, rows,width):
  gap = width // rows
  y , x = pos
  row = y//gap
  col = x//gap
  return row, col

def main(WINDOW, width):
  ROWS = 25
  grid = make_grid(ROWS,width)

  start = None
  end = None

  running = True
  started = False
  while running:
    draw(WINDOW,grid,ROWS,width)
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
      if started:
        continue
      if pygame.mouse.get_pressed()[0]:#left
        pos = pygame.mouse.get_pos()
        row,col = get_clicked_pos(pos,ROWS,WIDTH)
        Squares = grid[row][col]
        if not start and Squares != end:
          start = Squares
          start.make_start_square()
        elif not end and Squares != start:
          end = Squares
          end.make_end_square()
        elif Squares != end and Squares != start:
          Squares.make_barrier()

      elif pygame.mouse.get_pressed()[2]:#right
        pos = pygame.mouse.get_pos()
        row , col = get_clicked_pos(pos,ROWS,width)
        Squares = grid[row][col]
        Squares.reset()
        if Squares == start:
          start = None
        elif Squares == end:
          end = None

      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE and start and end:
          for row in grid:
            for Squares in row:
              Squares.update_neighbours(grid)#obtains neighbours

          algorithm(lambda: draw(WINDOW, grid, ROWS, width), grid, start, end)#lambda allows draw()to be an input
          
        if event.key == pygame.K_c:
          start = None 
          end = None
          grid = make_grid(ROWS, width)
				


  pygame.quit()

main(WINDOW,WIDTH)      
