
# https://github.com/chindesaurus/tetris/blob/master/tetris.py

'''
tetris.py

Usage: python tetris.py

@author chindesaurus
'''
from __future__ import division

from builtins import range
from past.utils import old_div
from builtins import object
from graphics import *
import random



############################################################
# CONFIG
############################################################


# normal mode on Air 15
my_BOARD_WIDTH = 10*8
my_BOARD_HEIGHT = 64 #112
my_DELAY = 100   #game frame speed in milliseconds
my_BOARD_MOVE_DELAY=20 # the board moves once in each # timesteps

my_BLOCK_SIZE = 12 #7 #30
my_OUTLINE_WIDTH = 2 #1 #3


COLUMN_COLOR = (['cyan']*5+['grey']*5)*8*2   #preset color for each column

# giant board
if False:
    my_BOARD_WIDTH = 10*16
    my_BOARD_HEIGHT = 110 #112
    my_BLOCK_SIZE = 7
    my_OUTLINE_WIDTH = 1

#small board
if True:
    my_COLUMN_HEIGHT = 10*2
    my_COLUMNS = 2
    my_BOARD_HEIGHT = my_COLUMN_HEIGHT * my_COLUMNS
    my_BOARD_WIDTH = 10*2
    #my_BOARD_HEIGHT = 30
    my_BLOCK_SIZE = 18
    my_OUTLINE_WIDTH = 2

if True:
    my_COLUMN_HEIGHT = 42
    my_COLUMNS = 2
    my_BOARD_HEIGHT = my_COLUMN_HEIGHT * my_COLUMNS
    my_BOARD_WIDTH = 10*4
    #my_BOARD_HEIGHT = 30
    my_BLOCK_SIZE = 16
    my_OUTLINE_WIDTH = 2    


    
############################################################
# BLOCK CLASS
############################################################

def xy2column(pos):
    pass
def transform_p(p):
    columns=2
    y = p.y % my_BPARD_HEIGHT

class Block(Rectangle):
    ''' Block class:
        Implement a block for a tetris piece
        Attributes: x - type: int
                    y - type: int

        Specifies the position on the tetris board
        in terms of the square grid.
    '''

    BLOCK_SIZE = my_BLOCK_SIZE #12 #7 #30
    OUTLINE_WIDTH = my_OUTLINE_WIDTH #2 #1 #3

    def __init__(self, pos, color):
        self.x = pos.x
        self.y = pos.y


        if self.y > my_COLUMN_HEIGHT+1:
            # shift one column to the right
            p1 = Point((pos.x+my_BOARD_WIDTH)*Block.BLOCK_SIZE + Block.OUTLINE_WIDTH,
                       (pos.y+2-my_COLUMN_HEIGHT)*Block.BLOCK_SIZE + Block.OUTLINE_WIDTH)
            p2 = Point(p1.x + Block.BLOCK_SIZE, p1.y + Block.BLOCK_SIZE)
        else:
            p1 = Point(pos.x*Block.BLOCK_SIZE + Block.OUTLINE_WIDTH,
                       (pos.y+2)*Block.BLOCK_SIZE + Block.OUTLINE_WIDTH)
            p2 = Point(p1.x + Block.BLOCK_SIZE, p1.y + Block.BLOCK_SIZE)



        Rectangle.__init__(self, p1, p2)
        self.setWidth(Block.OUTLINE_WIDTH)
        self.setFill(color)


    def can_move(self, board, dx, dy):
        ''' Parameters: dx - type: int
                        dy - type: int

            Return value: type: bool
                        
            Checks if the block can move dx squares in the x direction
            and dy squares in the y direction.
            Returns True if it can, and False otherwise.
        '''
        return board.can_move(self.x + dx, self.y + dy)
   
     
    def move(self, dx, dy):
        ''' Parameters: dx - type: int
                        dy - type: int
                        
            Moves the block dx squares in the x direction
            and dy squares in the y direction.
        '''
        self.x += dx
        self.y += dy

        if dy>1 or dy < -1:
            print(dy,'dy')
            
        shift_x = my_BOARD_WIDTH * Block.BLOCK_SIZE
        shift_y = (my_COLUMN_HEIGHT-1) * Block.BLOCK_SIZE
        if self.y == my_COLUMN_HEIGHT - 1 and dy > 0:
            Rectangle.move(self, shift_x, -shift_y) # shift right
        elif self.y == my_COLUMN_HEIGHT + 0 and dy < 0:
            Rectangle.move(self, -shift_x, shift_y) # shift left
        else:
            Rectangle.move(self, dx*Block.BLOCK_SIZE, dy*Block.BLOCK_SIZE)


############################################################
# SHAPE CLASS
############################################################

class Shape(object):
    ''' Shape class:
        Base class for all the tetris shapes
        Attributes: blocks - type: list - the list of blocks making up the shape
                    rotation_dir - type: int - the current rotation direction of the shape
                    shift_rotation_dir - type: Boolean - whether or not the shape rotates
    '''

    def __init__(self, coords, color):
        #self.coords=coords
        self.color=color

        #use random color
        #colors=['red','blue','yellow','cyan','orange','magenta']
        #self.color=random.choices(colors)
        
        self.blocks = []
        self.rotation_dir = -1
        ### A boolean to indicate if a shape shifts rotation direction or not.
        ### Defaults to false since only 3 shapes shift rotation directions (I, S and Z)
        self.shift_rotation_dir = False
        
        for pos in coords:
            self.blocks.append(Block(pos, self.color))

        left=10000
        right=-10000
        for pos in coords:
            if pos.x < left:
                left = pos.x
            if pos.x > right:
                right = pos.x
                
    def ref_draw(self,board):
        '''Add reference block in targeted position at bottom. Update when move left or right
        '''
        #get coords and duplicate the shape with transparent color (no Fill)
        coords=[]
        for block in self.blocks:
            coords.append(Point(block.x,block.y))        
        self.ref_shape=Shape(coords, self.color)
        for block in self.ref_shape.blocks:
            block.setWidth(Block.OUTLINE_WIDTH*2)
            block.setFill(None)
        # move the ref block to the bottom
        while self.ref_shape.can_move(board, 0, 1):
            self.ref_shape.move(0, 1)
        self.ref_shape.draw(board.canvas)
            
    def ref_undraw(self):
        '''Undraw the ref shape
        '''
        for block in self.ref_shape.blocks:
            block.undraw()
    
    def get_blocks(self):
        ''' Returns the list of blocks.
        '''
        return self.blocks


    def draw(self, win):
        ''' Parameter: win - type: CanvasFrame

            Draws the shape:
            i.e. draws each block.
        '''
        #self.ref_lines.draw(win)
        for block in self.blocks:
            block.draw(win)

    def undraw(self):
        for block in self.blocks:
            block.undraw()
        self.ref_undraw()

    def move(self, dx, dy):
        ''' Parameters: dx - type: int
                        dy - type: int

            Moves the shape dx squares in the x direction
            and dy squares in the y direction, i.e.
            moves each of the blocks.
        '''
        for block in self.blocks:
            block.move(dx, dy)
        #self.ref_lines.move(dx * (Block.BLOCK_SIZE),0)

    def can_move(self, board, dx, dy):
        ''' Parameters: dx - type: int
                        dy - type: int

            Return value: type: bool
                        
            Checks if the shape can move dx squares in the x direction
            and dy squares in the y direction, i.e.
            check if each of the blocks can move.
            Returns True if all of them can, and False otherwise.
        '''
        for block in self.blocks:
            if not(block.can_move(board, dx, dy)):
                return False 
        return True

 
    def get_rotation_dir(self):
        ''' Return value: type: int
        
            Returns the current rotation direction.
            1 indicates clockwise, -1 indicates counterclockwise
        '''
        return self.rotation_dir


    def can_rotate(self, board):
        ''' Parameters: board - type: Board object
            Return value: type : bool
            
            Checks if the shape can be rotated.
            
            1. Get the rotation direction using the get_rotation_dir method
            2. Compute the position of each block after rotation and check if
            the new position is valid
            3. If any of the blocks cannot be moved to their new position,
            return False
                        
            Otherwise all is good, return True.
        '''
        # the rotation direction
        rot_dir = self.get_rotation_dir() 

        # the center of the shape 
        center = self.blocks[1];

        # don't allow any of the blocks in the shape move
        # beyond the board boundaries or into an occupied square
        for block in self.blocks:
            x = center.x - rot_dir * center.y + rot_dir * block.y
            y = center.y + rot_dir * center.x - rot_dir * block.x
            if not(board.can_move(x, y)):
                return False

        return True


    def rotate(self, board):
        ''' Parameters: board - type: Board object

            Rotates the shape:
            1. Get the rotation direction using the get_rotation_dir method
            2. Compute the position of each block after rotation
            3. Move the block to the new position
        '''    
        # the rotation direction
        rot_dir = self.get_rotation_dir()
    
        # the center of the shape 
        center = self.blocks[1];

        if self.can_rotate(board):

            for block in self.blocks:
                x = center.x - rot_dir * center.y + rot_dir * block.y
                y = center.y + rot_dir * center.x - rot_dir * block.x
                if board.can_move(x, y):
                    block.move(x - block.x, y - block.y)

        ### Default behavior is that a piece will only shift
        ### rotation direction after a successful rotation. This ensures that 
        ### pieces which switch rotations definitely remain within their 
        ### accepted rotation positions.
        if self.shift_rotation_dir:
            self.rotation_dir *= -1

        

############################################################
# ALL SHAPE CLASSES
############################################################

 
class I_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x - 2, center.y),
                  Point(center.x - 1, center.y),
                  Point(center.x    , center.y),
                  Point(center.x + 1, center.y)]
        Shape.__init__(self, coords, 'blue')
        self.shift_rotation_dir = True
        self.center_block = self.blocks[2]

class J_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x - 1, center.y),
                  Point(center.x    , center.y),
                  Point(center.x + 1, center.y),
                  Point(center.x + 1, center.y + 1)]
        Shape.__init__(self, coords, 'orange')        
        self.center_block = self.blocks[1]

class L_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x - 1, center.y),
                  Point(center.x    , center.y),
                  Point(center.x + 1, center.y),
                  Point(center.x - 1, center.y + 1)]
        Shape.__init__(self, coords, 'cyan')        
        self.center_block = self.blocks[1]


class O_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x    , center.y),
                  Point(center.x - 1, center.y),
                  Point(center.x   , center.y + 1),
                  Point(center.x - 1, center.y + 1)]
        Shape.__init__(self, coords, 'red')
        self.center_block = self.blocks[0]

    def rotate(self, board):
        # Override Shape's rotate method since O_Shape does not rotate
        return 

class S_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x    , center.y),
                  Point(center.x    , center.y + 1),
                  Point(center.x + 1, center.y),
                  Point(center.x - 1, center.y + 1)]
        Shape.__init__(self, coords, 'green')
        self.center_block = self.blocks[0]
        self.shift_rotation_dir = True
        self.rotation_dir = -1


class T_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x - 1, center.y),
                  Point(center.x    , center.y),
                  Point(center.x + 1, center.y),
                  Point(center.x    , center.y + 1)]
        Shape.__init__(self, coords, 'yellow')
        self.center_block = self.blocks[1]


class Z_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x - 1, center.y),
                  Point(center.x    , center.y), 
                  Point(center.x    , center.y + 1),
                  Point(center.x + 1, center.y + 1)]
        Shape.__init__(self, coords, 'magenta')
        self.center_block = self.blocks[1]
        self.shift_rotation_dir = True
        self.rotation_dir = -1      



class Snake():
    '''Helper class to generate the bottom row
       Create a connected line, just like a snake
    '''
    def __init__(self,width,length=-1):
        self.width=width #int, width of the board
        if length==-1:   #the length of the allowed center region to generate the crack/snake
            #self.length = self.width//3
            self.length = 8            
        else:
            self.length=length
        # left and right boundary of the center region
        self.left = (self.width-self.length)//2
        self.right = self.left + self.length        
        #self.snake=[]
        #self.snake=[[0,10,0],[1,10,-1],[1,9,-1],[1,8,-1],[1,7,0]]
        self.snake=[[0, 10, 0], [1, 10, -1], [1, 9, -1], [1, 8, -1], [1, 7, 0], [2, 7, -1], [2, 6, 0], [3, 6, 0], [4, 6, 1], [4, 7, 0], [5, 7, 0], [6, 7, 1], [6, 8, 0], [7, 8, 0], [8, 8, 0], [9, 8, 0], [10, 8, 0], [11, 8, 1], [11, 9, 1], [11, 10, 0], [12, 10, 1], [12, 11, 0], [13, 11, 0]]
        # snake saves all the empty postion in the crack/snake
        #self.snake=[[46, 38, 1], [46, 39, 1], [46, 40, 0], [47, 40, 0], [48, 40, -1], [48, 39, -1], [48, 38, 0], [49, 38, 0], [50, 38, 1], [50, 39, 0]]
        # tuple format: (x,y,direction)
        # Direction: 0 for up, -1 for left, 1 for right
        print(f'Snake: left {self.left} right {self.right}, width {self.width}')

    def next(self):
        '''Return a list of empty sites in the next (new bottom) row
           The list will be appended into self.snake
        '''
        def next_point(p2,p3):
            '''Return a new point based on historical route
            '''
            p4=[0,0,0]
            allowed_directions=[-1,0,1]

            # limit the snake in center reigon
            if p3[1]>self.right:
                allowed_directions.remove(1)
            elif p3[1] < self.left:
                allowed_directions.remove(-1)

            # constraint from previous moving direction
            if p3[2] == 0: #was moving up
                p4[0] = p3[0] + 1 #add row index by one
                p4[1] = p3[1]                
                if p2[2] !=0:
                    try:
                        allowed_directions.remove(-p2[2]) #can not move back immediately
                    except:
                        pass
            else: # was moving left or right
                p4[0] = p3[0] #same row
                p4[1] = p3[1] + p3[2]
                try:
                    allowed_directions.remove(-p3[2])   # can not move back
                except:
                    pass

            # random output in allowed directions
            p4[2] = random.choice(allowed_directions)
            return p4
        empties=[]
        while True:
            p = next_point(self.snake[-2],self.snake[-1])            
            self.snake.append(p)
            empties.append(p[1])
            if p[2] == 0: # if move up, then this row is finished
                break
            # otherwise continue to generate new point
        #print(self.snake)  # print to get samples
        return empties

############################################################
# BOARD CLASS
############################################################

class Board(object):
    ''' Board class: it represents the Tetris board

        Attributes: width - type:int - width of the board in squares
                    height - type:int - height of the board in squares
                    canvas - type:CanvasFrame - where the pieces will be drawn
                    grid - type:Dictionary - keeps track of the current state of
                    the board; stores the blocks for a given position
    '''
    
    def __init__(self, win, width, height, dj):
        self.width = width
        self.height = height
        self.dj=dj #for playing sound while deleting row

        # create a canvas to draw the tetris shapes on
        self.canvas = CanvasFrame(win, self.width * Block.BLOCK_SIZE*2,
                                        (self.height/2+5) * Block.BLOCK_SIZE)
        self.canvas.setBackground('light gray')

        # create an empty dictionary
        # currently we have no shapes on the board
        self.grid = {}
        self.snake=Snake(self.width)

        # text to display game info
        info = Text(Point(800, 30), "Score: ")
        info.setSize(16)
        info.draw(self.canvas)
        self.info = info
        
        # record num of rows being deleted
        self.num_deleted_rows=0  

        # show instruction:
        _help_text="LEFT/RIGHT: move, UP: rotate, DOWN: drop"
        _help = Text(Point(160, 20), _help_text)
        _help.setSize(16)
        _help.draw(self.canvas)
        _=Text(Point(140, 40), "SPACE/m: magic block, A: grow bottom")
        _.setSize(16)
        _.draw(self.canvas)

    def draw_shape(self, shape):
        ''' Parameters: shape - type: Shape
            Return value: type: bool

            Draws the shape on the board if there is space for it
            and returns True, else returns False.
        '''
        if shape.can_move(self, 0, 0):
            shape.draw(self.canvas)
            return True
        return False


    def can_move(self, x, y):
        ''' Parameters: x - type:int
                        y - type:int
            Return value: type: bool

            1. Check if it is ok to move to square x,y
            if the position is outside of the board boundaries, can't move there
            return False.

            2. If there is already a block at that postion, can't move there
            return False.

            3. Otherwise return True.
            
        '''
        # boolean - is position x,y within the board boundaries?
        withinBoard = (x in range(Tetris.BOARD_WIDTH) and y in range(Tetris.BOARD_HEIGHT))

        # boolean - is there a block at position x,y?
        occupied = ((x, y) in self.grid)

        return (withinBoard and not occupied)


    def add_shape(self, shape):
        ''' Parameter: shape - type:Shape
            
            Add a shape to the grid, i.e.
            add each block to the grid using its
            (x, y) coordinates as a dictionary key.
        '''
        # the list of blocks
        listBlocks = shape.get_blocks()

        # add to dictionary: (x,y) coordinates as key, block as value
        for block in listBlocks:
            self.grid.update({(block.x, block.y):block})


    def delete_row(self, y):
        ''' Parameters: y - type:int

            Remove all the blocks in row y.
        '''
        # remove all blocks in row y from the grid
        # and undraw them

        #play sound
        self.dj.play(sound='delete_row')
        
        #add animation here
        delay=1
        colors=['red','blue','yellow','purple']
        for i in range(1):                
            for color in colors[:1]:
                for x in range(Tetris.BOARD_WIDTH):
                    self.grid[x, y].setFill(color)
                    #self.canvas.flush() #no delay for fast animation
                    self.canvas.after(delay,self.canvas.flush())

        # delete it
        for x in range(Tetris.BOARD_WIDTH):
            self.grid[x, y].undraw()
            del self.grid[x, y]

        # update score on screen
        self.num_deleted_rows += 1
        self.score()

        
 
    def is_row_complete(self, y):        
        ''' Parameter: y - type: int
            Return value: type: bool

            For each block in row y
            check if there is a block in the grid (use the in operator).
            If there is one square that is not occupied, return False
            otherwise return True.
        '''
        # for each block in row y
        for x in range(Tetris.BOARD_WIDTH):

            # if there is not a block in the row
            if not((x, y) in self.grid):
                return False
        return True
   
 
    def move_down_rows(self, y_start):
        ''' Parameters: y_start - type:int                        

            Moves all rows above y_start (inclusive) down one square.

            for each row from y_start to the top
                for each column
                    check if there is a block in the grid
                    if there is, remove it from the grid
                    and move the block object down on the screen
                    and then place it back in the grid in the new position
        '''
        for y in range(y_start, -1, -1):
            for x in range(Tetris.BOARD_WIDTH):
                if (x, y) in self.grid:
                    print(f"{(x,y)}",end = ',')

                    block = self.grid[(x, y)]
 
                    # remove it from the grid
                    del self.grid[(x, y)]

                    # move the block object down on the screen
                    block.move(0, 1)
    
                    # place block back in the grid in the new position
                    self.grid[(x, y + 1)] = block
                    

                    
    def _collapse_column(self,x,y):
        '''Collapse the column x for blocks above y
           Move blocks one by one
           This function is outdated. Save here for a record.
        '''        
        for i in range(y):
            yy = y-i  #check from this row and up
            if (x,yy) in self.grid:
                #move it down
                while self.can_move(x,yy+1):
                    _delay = 5
                    self.canvas.after(_delay,self.canvas.flush())
                    #print(f'moved {(x,yy)} to {(x,yy+1)}')
                    block = self.grid[(x, yy)]
                    del self.grid[(x, yy)]
                    block.move(0, 1)
                    self.grid[(x, yy + 1)] = block
                    yy = yy+1
                    
    def collapse_column(self,x,y):
        '''Collapse the column x for blocks above y
           Move all blocks at the same time
        '''
        flag_moved=False
        while True:
            for i in range(y):
                yy = y-i  #check from this row and up
                if (x,yy) in self.grid:
                    #move it down
                    if self.can_move(x,yy+1):
                        block = self.grid[(x, yy)]
                        del self.grid[(x, yy)]
                        block.move(0, 1)
                        self.grid[(x, yy + 1)] = block
                        flag_moved = True
                
            if not flag_moved:
                # end if nothing can be moved
                break
            else:
                # some blocks has been moved, animate it
                _delay = 100
                self.canvas.after(_delay,self.canvas.flush())
                flag_moved=False


    def collapse_row(self,y):
        '''For empty sites at row y, collapse the column
        '''
        start_collapse=False
        #after deleting the row, in the following row, find a column to collapse
        if y < self.height: #can not do for bottom row
                for x in range(self.width):
                    if (x,y) not in self.grid:
                        #found empty location
                        self.collapse_column(x,y)
                        start_collapse=True
                        #break # only collapse for once
                    else: # only continue collapsing for neighboring empty sites, and stops once reace an actual block. It looks like this is always the case
                        if start_collapse==True:
                            break
                        
    def move_up_rows(self):
        ''' Moves all rows up one square.

            for each block in grid
                move it up for one square
                save it in a new grid
                replace self.grid by the new grid
        '''
        new_grid={}
        for x,y in self.grid:
            block = self.grid[(x, y)]
            block.move(0, -1)
            new_grid[(x, y - 1)] = block
        #del self.grid
        self.grid = new_grid            

    def create_new_bottom(self):
        '''After moving board up, generate a new row in the bottom
        '''
        # Get empty sites in the new bottom row
        empties = self.snake.next()
        #print(empties)
        for x in range(Tetris.BOARD_WIDTH):
            if x not in empties:
                pos=Point(x,Tetris.BOARD_HEIGHT-1)
                #block=Block(pos, color='yellow')
                block=Block(pos, color=COLUMN_COLOR[x]) #assign color according to preset value in CONFIG
                block.draw(self.canvas)
                self.grid[(pos.x,pos.y)]=block
        
    def remove_complete_rows(self):
        ''' Removes all the complete rows
            1. for each row, y, 
            2. check if the row is complete
                if it is,
                    delete the row
                    move all rows down starting at row y - 1
        '''
        # for each row y
        for y in range(Tetris.BOARD_HEIGHT):
            
            # if the row is complete 
            if self.is_row_complete(y):
               
                # delete the row
                print(f'delete row {y}')
                self.delete_row(y)

                # move all rows down starting at row y - 1
                print(f'move rows down at {y-1}')
                self.move_down_rows(y - 1)

                # check the next row and collapse column with empty site
                self.collapse_row(y+1)

    def score(self):
        '''Display game info
        '''
        s=f'Score: {self.num_deleted_rows}'
        self.info.setText(s)
                
    def game_over(self):
        ''' Display "Game Over !!!" message in the center of the board
        '''
        message = Text(Point(150, 150), "Game Over !!!\n Thanks for playing.")
        message.setSize(32)
        message.draw(self.canvas)


############################################################
# TETRIS CLASS
############################################################

class Tetris(object):
    ''' Tetris class: Controls the game play
        Attributes:
            SHAPES - type: list (list of Shape classes)
            DIRECTION - type: dictionary - converts string direction to (dx, dy)
            BOARD_WIDTH - type:int - the width of the board
            BOARD_HEIGHT - type:int - the height of the board
            board - type:Board - the tetris board
            win - type:Window - the window for the tetris game
            delay - type:int - the speed in milliseconds for moving the shapes
            current_shape - type: Shape - the current moving shape on the board
            paused - type: boolean - whether or not the game is currently paused
    '''
    SHAPES = [I_shape, J_shape, L_shape, O_shape, S_shape, T_shape, Z_shape]
    DIRECTION = {'Left':(-1, 0), 'Right':(1, 0), 'Down':(0, 1)}
    BOARD_WIDTH = my_BOARD_WIDTH
    BOARD_HEIGHT = my_BOARD_HEIGHT 
    BOARD_MOVE_DELAY = my_BOARD_MOVE_DELAY
    
    def __init__(self, win):        
        self.dj = DJ() # sound control        
        self.board = Board(win, self.BOARD_WIDTH, self.BOARD_HEIGHT, self.dj)
        self.win = win
        self.delay = my_DELAY # milliseconds
        self.board_move_delay = Tetris.BOARD_MOVE_DELAY

        # sets up the keyboard events
        # when a key is called the method key_pressed will be called
        self.win.bind_all('<Key>', self.key_pressed)

        # set the current shape to a random new shape
        self.current_shape = self.create_new_shape()

        # draw the current_shape on the board
        Board.draw_shape(self.board, self.current_shape)

        self.current_shape.ref_draw(self.board)

        # the game is initially not paused
        self.paused = False

        # animate the shape!
        self.animate_shape()

        
        
    def create_new_shape(self,index=-1): #-1 for random shape, 0 for I shape
        ''' Return value: type: Shape
            
            Creates a random new shape that is centered
            at y = 0 and x = int(self.BOARD_WIDTH/2).
            Returns the shape.
        '''

        if index == -1:
            # generate a pseudorandom integer in this range (inclusive)
            index = random.randint(0, len(Tetris.SHAPES) - 1)
            
        # select a shape
        shape = Tetris.SHAPES[index]

        # center the shape at this point
        point = Point(int(old_div(self.BOARD_WIDTH, 2)), 2)

        ref = shape(point)
        if index == 0:
            ref.rotate(self.board)
        return ref
        '''
        if shape == I_shape:
            ref = I_shape(point)
        elif shape == J_shape:
            ref = J_shape(point)
        elif shape == L_shape:
            ref = L_shape(point)
        elif shape == O_shape:
            ref = O_shape(point)
        elif shape == S_shape:
            ref = S_shape(point)
        elif shape == T_shape:
            ref = T_shape(point)
        else:
            ref = Z_shape(point)

        # return a reference to the new Shape object
        return ref
        '''
    
    def animate_shape(self):
        ''' Animate the shape - move down at equal intervals
            specified by the delay attribute so long as the 
            game is not paused.
        '''
        if not self.paused:
            self.do_move('Down')
        self.win.after(self.delay, self.animate_shape)
   
 
    def do_move(self, direction):
        ''' Parameters: direction - type: string
            Return value: type: bool

            Move the current shape in the direction specified by the parameter:
            First check if the shape can move. If it can, move it and return True
            Otherwise if the direction we tried to move was 'Down',
            1. add the current shape to the board
            2. remove the completed rows if any 
            3. create a new random shape and set current_shape attribute
            4. If the shape cannot be drawn on the board, display a
               game over message

            Return False
        '''
        # get the x and y displacements from DIRECTION attribute
        displacement = self.DIRECTION.get(direction)
        x = displacement[0]
        y = displacement[1]

        # move the shape (if possible)
        if self.current_shape.can_move(self.board, x, y):
            if direction == 'Down':
                # move board up
                if self.board_move_delay < 1:
                    self.board_move_delay = Tetris.BOARD_MOVE_DELAY
                    self.board.move_up_rows()
                    self.board.create_new_bottom()
                    self.current_shape.ref_shape.move(0, -1)
                else:
                    self.board_move_delay -= 1
            else: #left or right
                self.current_shape.move(x, y)
                self.current_shape.ref_undraw()
                self.current_shape.ref_draw(self.board)


            return True

        # else the piece has hit the bottom
        else:
            # if the last failed move was Down
            if direction == 'Down':

                # clear previous ref shape in the bottom
                self.current_shape.ref_undraw()
                
                # add the current shape to the board
                self.board.add_shape(self.current_shape)

                # remove completed rows (if any)
                self.board.remove_complete_rows()


                # update Tetris.current_shape with a new random shape
                self.current_shape = self.create_new_shape()

                # update new ref shape
                self.current_shape.ref_draw(self.board)
                
                # draw the new shape on the board
                # if not possible, then the game is over
                if not self.board.draw_shape(self.current_shape):
                    self.board.game_over()
                return False
            

    def do_rotate(self):
        ''' Checks if the current_shape can be rotated and
            rotates if it can.
        '''
        self.current_shape.rotate(self.board)
        self.current_shape.ref_undraw()
        self.current_shape.ref_draw(self.board)
 
    def key_pressed(self, event):
        ''' This function is called when a key is pressed on the keyboard.

            If the user presses the arrow keys
            'Left', 'Right' or 'Down', the current_shape will move in
            the appropriate direction.

            If the user presses the space bar 'space', the shape will move
            down until it can no longer move and is added to the board.

            If the user presses the 'Up' arrow key,
            the shape rotates.
        '''
        key = event.keysym
        #print key   # for debugging

        if not self.paused:
            # play sound for key event
            self.dj.play()

            # move left, right, and down
            #if key in self.DIRECTION: 
            if key in ['Left','Right']: #not down anymore                
                self.do_move(key)
            if key == 's': #speed up the game manually
                for i in range(10):
                    self.do_move('Down')
            if key == 'a': #more speed up the game manually
                for i in range(100):
                    self.do_move('Down')
                
            # drop piece
            elif key == "Down":
                while (self.current_shape.can_move(self.board, 0, 1)):
                    self.current_shape.move(0, 1)

            # rotate 
            elif key == "Up":
                self.do_rotate()

            # magic key to get I shape
            elif key =="m" or key == "space":
                self.current_shape.undraw()
                del self.current_shape
                self.current_shape = self.create_new_shape(0)
                if not self.board.draw_shape(self.current_shape):
                    self.board.game_over()
                self.current_shape.ref_draw(self.board)
                

                
        # pause and unpause the game
        if key == 'p' or key == 'P':
            self.paused = not self.paused
            # display the status in window title
            if self.paused:
                self.win.title('Tetris  Paused')
            else:
                self.win.title('Tetris')


# filename for the sound                
soundfiles={'key':'menuselect.mp3',
            'delete_row':'giftbox.mp3',            
#            'delete_row':'gift_short.mp3',
            }

from playsound import playsound
import threading

class DJ():
    '''The DJ to control all sound
    '''
    def __init__(self):
        # keep an record of previous thread and sound
        self.thread0=None
        self.sound0=None

    
    def play_after(self,thread0=None,soundfile='menuselect.mp3'):
        '''Function to be called in a thread to play the sound
        '''
        # wait for previous thread to finish, then play
        if thread0:            
            #print('thread0.is_alive()',thread0.is_alive())
            thread0.join()
        playsound(soundfile)
        #playsound('menuselect.mp3')

    def play(self,sound='key'): #only play after previous sound
        if self.thread0:
            #print('self.thread0.is_alive()',self.thread0.is_alive())
            if self.thread0.is_alive():
                if sound == self.sound0:
                    #skip for same sound
                    return
                else:
                    #play for different sound
                    pass

        # only play when previous sound is finished, or is different
        soundfile = soundfiles[sound]
        thread = threading.Thread(target=self.play_after, args=(self.thread0,soundfile,))
        thread.start()
        self.thread0=thread
        self.sound0=sound        

        

################################################################
# Start the game
################################################################

win = Window("Tetris")
game = Tetris(win)
win.mainloop()
