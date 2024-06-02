# game shutu
# from the app shudu (sodoku)

# config
n = 15  #board size n by n

import random

def transpose(board):
    t = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            t[i][j] = board[j][i]
    return t

def print_board(board):
    for _ in board:
        print(_)

def print_game(board, left_lengths, top_lengths):
    max_lengths = 5
    L = n + max_lengths
    game = [[ 0 for _ in range(L) ] for _ in range(L)]
    # assign board
    for i in range(n):
        for j in range(n):
            ii=i + max_lengths
            jj=j + max_lengths
            game[ii][jj]=board[i][j]
    for i in range(n):
        lengths = left_lengths[i]
        num = len(lengths)
        for j in range(num):
            game[max_lengths + i][j]=lengths[j]
    for j in range(n):
        lengths = top_lengths[j]
        num = len(lengths)
        for i in range(num):
            game[i][max_lengths + j]=lengths[i]
        
        
    print_board(game)
            
def list2length(row):
    lengths=[]
    length=0
    for i in row:
        if i==1:
            length +=1
        else: #i==0
            if length==0:
                pass
            else:
                lengths.append(length)
                length = 0
    if length>0:
        lengths.append(length)
    if len(lengths) == 0:
        print('got zero list for ',row)
        exit()
    return lengths

def row_lengths(board):
    left_lengths=[]
    for row in board:
        left_lengths.append(list2length(row))
    return left_lengths

#generate the same
def gen():
    board=[[ random.randint(0,1) for _ in range(n)] for _ in range(n)]
    print_board(board)

    left_lengths = row_lengths(board)
    print(left_lengths)
    board_t = transpose(board)
    top_lengths = row_lengths(board_t)
    print(top_lengths)
    print_game(board, left_lengths, top_lengths)

def solve():
    pass
def step():
    pass

def main():
    pass


gen()
