#! /usr/bin/env python
import random
import re #regular expression libary
import time
from string import ascii_lowercase

#Setting up a defualt grid
def setUpGrid(grid_size, number_of_mines):
    default_grid = [['0' for i in range(grid_size) ] for i in range(grid_size)]
    mines = getMines(default_grid, number_of_mines)

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
def getMines(grid, number_of_mines):
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
def revealBlocks(opened_blocks, grid, game_board, row, col):
    #if the block has NOT been revealed already
    if game_board[row][col] == '?':
        game_board[row][col] = grid[row][col]
	opened_blocks.append((row, col))
        if grid[row][col] == '0':
            for r, c in findNeighbours(grid, row, col):
                revealBlocks(opened_blocks, grid, game_board, r, c)
    else:
        return

#Validate user input and return with proper coordinate and msg
def validateInput(grid, promp):
    grid_size = len(grid)
    invalid_input_msg = '\n >>>Wrong Input Value!! \n'
    coordinate = ()

    pattern = r'([a-{}])([0-9]+)(f?)'.format(ascii_lowercase[grid_size - 1])
    valid_input = re.match(pattern, promp)
    
    #If the input is validated with the regex and in the grid
    if valid_input or int(valid_input.group(2)) <= (grid_size - 1):
        col_num = ascii_lowercase.index(valid_input.group(1))
        row_num = int(valid_input.group(2))
	flag = valid_input.group(3)
        coordinate = (row_num, col_num)
        invalid_input_msg = ''

    return {'coordinate': coordinate, 'flag':flag, 'msg': invalid_input_msg}

#Promped Grid Size from User
def prompedGridInfo():
    grid_info = ()
    try:
	grid_size = input("Enter the size of the game board(just the width): ")
	number_of_mines = input("Enter the number of mines(the number shoud be smaller than {}): ".format(grid_size ** 2))
	if number_of_mines >= (grid_size ** 2):
	    print "\n >>>Number of mines has to be smaller than the board size {}!! \nPLEASE TRY AGAIN".format(grid_size ** 2)
	else:
	    grid_info = (grid_size, number_of_mines)
    except NameError:
	print "\n >>>Please input an numeracal numbers(E.g. 1 ~ 99 )!! \nPLEASE TRY AGAIN"

    return grid_info

#Main Game
def playGame():
    start_time = 0
    input_grid_info = ()
    all_flags = []
    
    while len(input_grid_info) is 0:
	input_grid_info = prompedGridInfo()
    
    grid_size, number_of_mines = input_grid_info
    opened_blocks = []
    grid, mines = setUpGrid(grid_size,  number_of_mines)

    game_board = [['?' for i in range(grid_size) ] for i in range(grid_size)]
    displayGrid(game_board)


    Test = True

    msg = ("Please enter the coordinate (E.g. \"a0\" to revel the block or \"a0f\" for set/remove a flag): ")
    while Test == True:
	start_time - time.time();
        unopen_blocks = (grid_size ** 2 - len(opened_blocks) - number_of_mines)
	
	#Winner Check
	if (unopen_blocks is 0) or (set(all_flags) == set(mines)):
	    minues, seconds = divmod(int(time.time() - start_time), 60)
	    print "\n\n	WINNER!!! You solved in {} minues, and {} seconds".format((minues % 60), seconds)
	    return

        print '"', unopen_blocks, '"', 'blocks left to open!!'
        promp = raw_input(msg)
        result = validateInput(grid, promp)

        input_coordinate = result['coordinate']
	#Validate input(coordinate)
        if input_coordinate:
	    #If the block has never being revealed
	    if game_board[int(input_coordinate[0])][int(input_coordinate[1])] == '?': 
		#If the user wants to put flag on the block
		if result['flag']:
		    #If the block already has a flag
		    if grid[int(input_coordinate[0])][int(input_coordinate[1])] == 'F':
			all_flags.remover(result['coordinate'])
			game_board[int(input_coordinate[0])][int(input_coordinate[1])] = '?'
		    else:
			all_flags.append(result['coordinate'])
			game_board[int(input_coordinate[0])][int(input_coordinate[1])] = 'F'
			displayGrid(game_board)
	        elif grid[int(input_coordinate[0])][int(input_coordinate[1])] == 'X':
		    print '\n \n	GAME OVER!!! CHECK THE ANSWER BOARD BELOW ;)'
		    displayGrid(grid)
                    return
		else:
             	    revealBlocks(opened_blocks, grid, game_board, input_coordinate[0], 
		    input_coordinate[1])
		    displayGrid(game_board)
	    else:
		 print '\n >>>The block is already opened, please enter the new coordinate!! \nPLEASE TRY AGAIN'
	else:
	    print result['msg']	
playGame()
