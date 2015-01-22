#! /usr/bin/env python
import random
import re #regular expression libary
import time
from string import ascii_lowercase

#Setting up a defualt grid
def setUpGrid(grid_size, start, number_of_mines):
    default_grid = [['0' for i in range(grid_size) ] for i in range(grid_size)]
    mines = getMines(default_grid, start, number_of_mines)

    for i, j in mines:
        default_grid[i][j] = 'X'

    grid = setNumbers(default_grid)

    return (grid, mines)

#Display Grid with row # and colunm #
def displayGrid(grid):
    grid_size = len(grid)
    top_label = '     '

    #Horizontal division line in the grid
    horizontal_div_line = '    ' + (4 * grid_size * '-')

    #Print alphabet label on top
    for alphabet in ascii_lowercase[:grid_size]:
        top_label = top_label + alphabet + '   '

    print top_label, '\n', horizontal_div_line

    #Print grid with vertical numerical label
    for index, element in enumerate(grid):
	row = '{0:2} |'.format(index)	#format() after Python2.6 == '%s'
	for value in element:
	    row = row + ' ' + value + ' |'
        print row, '\n', horizontal_div_line
    print('')

#Get mines
def getMines(grid, start, number_of_mines):
    mines = []

    for i in range(number_of_mines):
	coordinate = getRandomCell(grid)
        while coordinate == coordinate in mines:
	    coordinate = getRandomCell(grid)
	mines.append(coordinate)
    return mines

#Find neighbours of input location
def findNeighbours(grid, num_row, num_col):
    grid_size = len(grid)
    neighbours = []

    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            elif (-1 < (num_row + i) < grid_size and -1 < (num_col + j) <
            grid_size):
                neighbours.append((num_row + i, num_col + j))
    return neighbours

#Get Rondom Cell Coordinate
def getRandomCell(grid):
    grid_size = len(grid)
    a = random.randint(0, grid_size - 1)
    b = random.randint(0, grid_size - 1)
    return (a, b)

#Set Number(s) in the grid corresponding to number of mine(s) in the neighbour
def setNumbers(grid):
    for row_num, row_element in enumerate(grid):
        for col_num, block in enumerate(row_element):
            if block != 'X':
                #Find all the neighours
                values = [grid[row][col] for row, col in findNeighbours(grid,
                    row_num, col_num)]
                #Insert number of mines around the current location
                grid[row_num][col_num] = str(values.count('X'))
    return grid
#Reveal blocks (copying value from grid(ans) to game board for display)
def revealBlocks(grid, game_board, row, col):
    #if the block has NOT been revealed already
    if game_board[row][col] == ' ':
        game_board[row][col] = grid[row][col]
        if game_board[row][col] == '0':
            for r, c in findNeighbours(grid, row, col):
                revealBlocks(grid, game_board, r, c)
    else:
        return

#Validate user input and return with proper coordinate and msg
def validateInput(grid, input):
    grid_size = len(grid)
    invalid_input_msg = 'Wrong Input Value'
    coordinate = ()

    pattern = r'([a-{}])([0-9]+)(f?)'.format(ascii_lowercase[grid_size - 1])
    valid_input = re.match(pattern, input)

    if valid_input:
        col_num = ascii_lowercase.index(valid_input.group(1))
        row_num = int(valid_input.group(2))
        coordinate = (row_num, col_num)
        invalid_input_msg = ''

    return {'coordinate': coordinate, 'msg': invalid_input_msg}

#Main Game
def playGame():
    grid_size = int(raw_input("Enter the size of the game board: "))
    number_of_mines = int(raw_input("Enter the number of mines: "))
    start = 0
    grid, mines = setUpGrid(grid_size, start, number_of_mines)

    game_board = [[' ' for i in range(grid_size) ] for i in range(grid_size)]
    displayGrid(game_board)

    Test = True
    msg = ("Please enter the coordinate: ")

    print "CHEEZE \n"
    displayGrid(grid)
    print "\n\n"

    while Test == True:
        input = raw_input(msg)
        result = validateInput(grid, input)

        input_coordinate = result['coordinate']

        if input_coordinate:

             revealBlocks(grid, game_board, input_coordinate[0],
                     input_coordinate[1])

             displayGrid(game_board)
playGame()
