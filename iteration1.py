#!/usr/bin/env python3
import random
import time

class Board:
    def __init__(self,side_length):
        self.open_space = []
        for r in range(side_length):
            for c in range(side_length):
                self.open_space.append("{}{}".format(chr(c + 97),str(r+1)))
        self.grid = [["."] * side_length for i in range(side_length)]

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
        
    def updateBoard(self,color,move) -> None:
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

    def getMove(color):
        return random.choice(self.possibleMoves(color))
  


#actual code running

#setup
line = '...'
bot_color = ''
bw = input()
if line == 'b':
    bot_color = 'b'
elif line == 'w':
    bot_color = 'w'
main_board = Board(8)

print('ok', flush=True)
while line and line != 'done':
  line = input()
  if line == 'get move':
    #start_time = time.time()
    print(main_board.getMove(bot_color), flush=True)
    #print("--- %s seconds ---" % (time.time() - start_time))
  elif line == 'done':
    pass
  else:
    words = str.split(line)
    main_board.updateBoard(words[1],words[2])
    main_board.printGrid()
    