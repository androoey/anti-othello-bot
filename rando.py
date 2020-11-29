#!/usr/bin/env python3
import random
#bw = input()
#print('ok', flush=True)

grid = [["."] * 8 for i in range(8)]
open_space = []

for r in range(8):
  for c in range(8):
    open_space.append("{}{}".format(chr(c + 97),str(r+1)))


def printGrid(board):
  print("    a b c d e f g h ")
  print("  +-----------------+")
  for row in range(8):
    print("{} {}".format(row + 1,"|"), end = " ")
    for col in range(8):
      print(board[row][col], end = " ")
    print("|")
  print("  +-----------------+")

def isValidMove(color,move,board):
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
      current = board[curr_row][curr_col] #string

      #check if theres something to sandwich
      if (curr_row + r < 0 or curr_row + r > 7 or curr_col + c < 0 
          or curr_col + c > 7 or board[curr_row + r][curr_col + c] != opposite):
        #print("{} {} failed".format(r,c))
        continue

      curr_row += r 
      curr_col += c

      while(not (curr_row == 0 and curr_col == 0) and curr_row >= 0 and curr_row <= 7
        and curr_col >= 0 and curr_col <= 7):
        current = board[curr_row][curr_col]
        if current == color:
          return True
        curr_row += r 
        curr_col += c
  return False
        


def updateBoard(color,move,board):
    opposite = ''
    if color == 'w':
      opposite = 'b'
    else:
      opposite = 'w'
    
    curr_row = int(move[1]) - 1
    curr_col = ord(move[0]) - 97

    valid_move = isValidMove(color,move,board)
    #if not valid_move:
    #  raise Exception("Not a valid move")done
      
    for r in range(-1,2):
      for c in range(-1,2):
        current = board[curr_row][curr_col] #string

        row = curr_row + r
        col = curr_col + c
        flip_array = []

        while(not (r == 0 and c == 0) and row >= 0 and row <= 7
            and col >= 0 and col <= 7):
          current = board[row][col]
          if current == color:
            for (flip_row,flip_col) in flip_array:
              board[flip_row][flip_col] = color
            break
          elif current == opposite:
            flip_array.append((row,col))
          else:
            break
          row += r 
          col += c
      
    board[curr_row][curr_col] = color
    open_space.remove(move)


def possibleMoves(color,board):
  moveset = []
  for move in open_space:
    if isValidMove(color,move,board):
      moveset.append(move)
  return moveset

def getMove(color,board):
  return random.choice(possibleMoves(color,board))

#if not isValidMove('w','d6',grid):
#  print("TEST 1 FAILED!")
#if not isValidMove('w','f8',grid):
#  print("TEST 2 FAILED!")

#if isValidMove('w','h1',grid):
#  print("TEST 3 FAILED!")
#printGrid(grid)
#updateBoard('b','f4',grid)
#moo = possibleMoves('w',grid)
#for e in moo:
#  print(e,end = ", ")
#print()
#print("selected move is" + getMove('w',grid))
#printGrid(grid)

bot_color = ''
line = '...'
while line and line != 'done':
  line = input()
  if line == 'b':
    bot_color = 'b'
  elif line == 'w':
    bot_color = 'w'
  elif line == 'get move':
    print(getMove(bot_color,grid), flush=True)
  elif line == 'done':
    pass
  else:
    words = str.split(line)
    updateBoard(words[1],words[2],grid)
    #printGrid(grid)
    