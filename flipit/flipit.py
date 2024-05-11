#play the game for flip it
# Author: Weilei Zeng
# Dated: May 10, 2024

from graphics import *
from button import Button
import random
import time
import numpy as np


def get_neighbors(rows,cols,board):
    #return neighbors of each plaquette. This takes care of the boundary condition
    neighbors=[]
    #placeholder=[[1 for _ in range(cols)] for _ in range(rows)]
    for i in range(rows):
            _=[]
            for j in range(cols):
                neighbor=[(i,j),(i+1,j),(i-1,j),(i,j+1),(i,j-1)]
                for xy in neighbor:
                    x,y=xy
                    if x < 0 or x > rows-1 or y < 0 or y > cols-1:
                        #print('remove ',xy,'from',neighbor)
                        neighbor.remove(xy)
                for xy in neighbor:#double check. very strange, cannot remove (0,6) from last for loop
                    x,y=xy
                    try:
                        board[x][y]
                        #print(i,jself.board[i][j])
                    except:
                        #print(neighbor)
                        #print(xy,self.cols)
                        #print(x < 0 or x > self.rows-1 or y < 0 or y > self.cols-1)
                        #print(xy,'is out of board')
                    #if x < 0 or x > self.rows-1 or y < 0 or y > self.cols-1:
                        #print('remove ',xy,'from',neighbor)
                        neighbor.remove(xy)
                        #print(neighbor)
                _.append(neighbor)
            neighbors.append(_)
    return neighbors


#convert index of 2D array to that of a horizontally stacked vector
def ij2index(i,j,rows,cols):
    return i*cols+j

#return parity check for graph defined by neighbors
#there are multiple ways to get H. for example, using non-cyclic shift matrix S, H = I * I + I * S + S * I + S^T * I + I * S^T
def get_H(neighbors,rows,cols):
    H_size = rows*cols
    H = np.zeros((H_size,H_size), dtype=int)
    print(H)
    for i in range(rows):
        for j in range(cols):
            index_i = ij2index(i,j,rows,cols)
            neighbor = neighbors[i][j]
            for n in neighbor:
                x,y=n
                index_j = ij2index(x,y,rows,cols)
                H[index_i][index_j]=1
    return H

#play the game on this board
class Board():
    def __init__(self,win,rows,cols):
        self.win=win
        self.rows=rows
        self.cols=cols
        # set a random initial board
        self.board = [[random.randint(0,1) for _ in range(self.cols)] for _ in range(self.rows)]
        #draw buttons/plaquettes and set up color accordingly
        self.buttons=[ [None for _ in range(self.cols)] for _ in range(self.rows) ]
        x0,y0=200,40 #top left anchor
        size,distance=60,10 #for each plaquette
        self.win.autoflush=False #turn it off for quick draw with many changes in the window
        for i in range(self.rows):
            for j in range(self.cols):
                button_plaquette = Button(self.win,
                                          center=Point(x0+(size+distance)*j,y0+(size+distance)*i),
                                          width=size, height=size, label=f"({i},{j})")
                #button_plaquette.face=1
                button_plaquette.activate()
                #button_plaquette.face=self.board[i][j]
                button_plaquette.i = i
                button_plaquette.j = j
                #print(button_plaquette.i,button_plaquette.j)
                if self.board[i][j]:
                    button_plaquette.rect.setFill('green')
                self.buttons[i][j] = button_plaquette

        self.win.flush()

        self.neighbors=get_neighbors(rows,cols,self.board)   
        self.H=get_H(self.neighbors,self.rows,self.cols)

        #self.push2right()
        #self.solve()
        
    def flip(self,r,c):
        # if (r,c) gets clicked
        neighbor = self.neighbors[r][c]
        #print('the neighbor for ',r,c,'is',neighbor)
        #flip all neighbors
        for n in neighbor:
            i,j=n
            #print('now check neighbor',i,j)
            if self.board[i][j] == 1:
                self.board[i][j] = 0
                self.buttons[i][j].rect.setFill('lightgray')
            else:
                self.board[i][j] = 1
                self.buttons[i][j].rect.setFill('green')
        #self.print()
                
    def print(self): #print the board in std
        print('--------------------------')
        for i in self.board:
            print(i)
        print('--------------------------')
    def check(self): #check if the whole board is cleaned. now just do it by hand
        pass

    def push2right(self):#push all plaquettes to the rightmost column
        for j in range(self.cols-1):#check column first
            for i in range(self.rows):
                if self.board[i][j]:
                    self.buttons[i][j+1].rect.setFill('yellow') #click the next column based on current column, this will clean the current column. Hence the loop push all colored plaquettes to the right most column
                    #self.win.flush()
                    #time.sleep(0.1)
                    self.flip(i,j+1)
                    self.win.flush()
                    #time.sleep(0.1)
                    
    def solve(self):# solve it using linear algebra
        e_array=np.array(self.board)
        print('current error\n',e_array)
        e = np.hstack(e_array)
        #print(self.H)

        s=np.linalg.solve(self.H,e)
        #print(s)

        import galois
        def binary_solve(A,b):
            GF = galois.GF(2)            #A = GF.Random((4,4))
            A=GF(A)
            b=GF(b)
            x = np.linalg.solve(A, b)
            return x 

        s2=binary_solve(self.H,e)
        #print('attemplt solution',s2)
        s3=s2.reshape(self.rows,self.cols)
        print('solution:\n',s3)
        #print('rank of H is ',np.linalg.matrix_rank(self.H))
        #display in color
        for i in range(self.rows):
            for j in range(self.cols):
                b=self.buttons[i][j]
                if s3[i][j]:
                    b.rect.setWidth(3)
                else:
                    b.rect.setWidth(1)        

    def shuffle(self):#generate random board and update all buttons
        self.board = [[random.randint(0,1) for _ in range(self.cols)] for _ in range(self.rows)]
        for i in range(self.rows):
            for j in range(self.cols):
                b=self.buttons[i][j]
                b.rect.setWidth(1)
                if self.board[i][j]:
                    b.rect.setFill('green')
                else:
                    b.rect.setFill('lightgray')                    
        
def main():
    win_width, win_height=1200,700+40
    img_width,img_height=win_width, win_height
    win = GraphWin('Flip it!', win_width, win_height)
    win_center=Point(win_width//2,600//2)

    button_push = Button(win, center=Point(60,60), width=100, height=30, label="Push to right")
    button_push.activate()
    button_shuffle = Button(win, center=Point(60,120), width=100, height=30, label="shuffle")
    button_shuffle.activate()
    button_solve = Button(win, center=Point(60,180), width=100, height=30, label="solve")
    button_solve.activate()
    button_exit = Button(win, center=Point(60,240), width=100, height=30, label="exit")
    button_exit.activate()

    #board = Board(win,5,6) #solution: pish to right, then duplicate the right col on the left
    board = Board(win,10,12)
    #board = Board(win,20,24)


    docstr='Click on a plaquette, its neighbors will get flipped, as well as itself. Try to flip all plaquettes!'
    doc=Text(Point(480,win_height-20),docstr)
#    doc.setText(
    doc.draw(win)


    board.win.autoflush=False
    while (True):
        p = win.getMouse()
        #print('clicked on ',p)
        if button_push.clicked(p):            
            #print('push')
            board.push2right()
        elif button_shuffle.clicked(p):
            board.shuffle()
        elif button_solve.clicked(p):
            board.solve()
        elif button_exit.clicked(p):
            win.close()
            break
        for bs in board.buttons:
            for b in bs:
                #print('now check button',b)
                if b.clicked(p):
                    #print('clicked on ',b,b.label,b.i,b.j)
                    board.flip(b.i,b.j)

        board.win.flush()
    print('Exit from the game.')
        
main()
