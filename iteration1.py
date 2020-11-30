#!/usr/bin/env python3
import random
import time
import math
import copy
from typing import Tuple,List

search_depth = 3

def opposite(color):
    if color == 'w':
        return 'b'
    else:
        return 'w'

class Board:
    def __init__(self,side_length,grid):
        self.grid = []
        if grid is not None:
            self.grid = copy.deepcopy(grid)
        else:
            self.grid = [["."] * side_length for i in range(side_length)]
        self.open_space = []
        for r in range(side_length):
            for c in range(side_length):
                if self.grid[r][c] == '.':
                    self.open_space.append("{}{}".format(chr(c + 97),str(r+1)))
        self.side_length = side_length

    def getGrid(self) -> List[List[str]]:
        return self.grid

    def printGrid(self):
        print("    a b c d e f g h ")
        print("  +-----------------+")
        for row in range(8):
            print("{} {}".format(row + 1,"|"), end = " ")
            for col in range(8):
                print(self.grid[row][col], end = " ")
            print("|")
        print("  +-----------------+")

    def isValidMove(self,color,move) -> bool:
        move_row = int(move[1]) - 1
        move_col = ord(move[0]) - 97

        opposite = ''
        if color == 'w':
            opposite = 'b'
        else:
            opposite = 'w'

        for r in range(-1,2):
            for c in range(-1,2):
                curr_row = move_row
                curr_col = move_col
                current = self.grid[curr_row][curr_col] #string

                #check if theres something to sandwich
                if (curr_row + r < 0 or curr_row + r > 7 or curr_col + c < 0 
                    or curr_col + c > 7 or self.grid[curr_row + r][curr_col + c] != opposite):
                    continue

                curr_row += r 
                curr_col += c

                while(not (curr_row == 0 and curr_col == 0) and curr_row >= 0 and curr_row <= 7
                    and curr_col >= 0 and curr_col <= 7):
                    current = self.grid[curr_row][curr_col]
                    if current == color:
                        return True
                    curr_row += r 
                    curr_col += c
        return False
        
    def updateBoard(self,color,move):
        opposite = ''
        if color == 'w':
            opposite = 'b'
        else:
            opposite = 'w'
        
        curr_row = int(move[1]) - 1
        curr_col = ord(move[0]) - 97

        for r in range(-1,2):
            for c in range(-1,2):
                current = self.grid[curr_row][curr_col] #string

                row = curr_row + r
                col = curr_col + c
                flip_array = []

                while(not (r == 0 and c == 0) and row >= 0 and row <= 7
                    and col >= 0 and col <= 7):
                    current = self.grid[row][col]
                    if current == color:
                        for (flip_row,flip_col) in flip_array:
                            self.grid[flip_row][flip_col] = color
                        break
                    elif current == opposite:
                        flip_array.append((row,col))
                    else:
                        break
                    row += r 
                    col += c
        
        self.grid[curr_row][curr_col] = color
        self.open_space.remove(move)

    def possibleMoves(self,color):
        moveset = []
        for move in self.open_space:
            if self.isValidMove(color,move):
                moveset.append(move)
        return moveset

    def gameOver(self) -> bool:
        return len(self.possibleMoves('w')) == 0 and len(self.possibleMoves('b')) == 0

    #returns number of black and white
    def countPieces(self) -> Tuple[int,int]:
        black,white = 0,0
        for row in range(self.side_length):
            for col in range(self.side_length):
                if self.grid[row][col] == 'b':
                    black += 1
                elif self.grid[row][col] == 'w':
                    white += 1
        return (black,white)

def heuristic(board) -> int:
    (black,white) = board.countPieces()
    return black - white

def min(board,color,depth) -> Tuple[str,int]:
    finished = board.gameOver()
    if finished:
        (black,white) = board.countPieces()
        return ("game over",black - white)

    choices = board.possibleMoves(color)
    (best_move,best_score) = ('',math.inf)
    for move in choices:
        #print("move considered: " + move)
        new_board = Board(8,board.getGrid())
        new_board.updateBoard(color,move)
        temp = 0
        if depth == 0:
            temp = heuristic(new_board)
            #print("score is: ",end = '')
            #print(temp)
            #new_board.printGrid()
        else:
            (rando,temp) = max(new_board,opposite(color),depth - 1)
        if temp < best_score:
            best_move = move
            best_score = temp
    return (best_move,best_score)

def max(board,color,depth) -> Tuple[str,int]:
    finished = board.gameOver()
    if finished:
        (black,white) = board.countPieces()
        return ("game over",black - white)

    choices = board.possibleMoves(color)
    (best_move,best_score) = ('',-math.inf)
    for move in choices:
        new_board = Board(8,board.getGrid())
        new_board.updateBoard(color,move)
        temp = 0
        if depth == 0:
            temp = heuristic(board)
        else:
            (rando,temp) = min(new_board,opposite(color),depth - 1)
        if temp > best_score:
            best_move = move
            best_score = temp
    return (best_move,best_score)

def getMove(board,color) -> str:
    if color == 'b':
        (move,score) = min(board,color,search_depth)
        return move
    else:
        (move,score) = max(board,color,search_depth)
        return move
  


#actual code running

#setup
line = '...'
bot_color = input()

main_board = Board(8,None)
#main_board.updateBoard('b','d4')
#main_board.updateBoard('w','e4')
#main_board.updateBoard('w','f4')
#main_board.updateBoard('b','d3')
#main_board.printGrid()

print('ok', flush=True)
while line and line != 'done':
  line = input()
  if line == 'get move':
    start_time = time.time()
    print(getMove(main_board,bot_color), flush=True)
    print("--- %s seconds ---" % (time.time() - start_time))
  elif line == 'done':
    pass
  else:
    words = str.split(line)
    main_board.updateBoard(words[1],words[2])
    main_board.printGrid()
    