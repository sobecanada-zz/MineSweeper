#! /usr/bin/env python
import random
import re #regular expression libary
import time
from string import ascii_lowercase

#Setting up a defualt grid
def setUpGrid(grid_size, start, number_of_mines):
    default_grid = [['0' for i in range(grid_size) ] for i in range(grid_size)]
    grid = default_grid;
    return grid

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
    for index, i in enumerate(grid):
	row = '{0:2} |'.format(index + 1)	#format() after Python2.6 == '%s'
	for j in i:
	    row = row + ' X ' + '|'
        print row, '\n', horizontal_div_line
    print('')

#Get mines
#def getMines(grid, start, number_of_mines):

#Find neighbours of input location
#def findNeighbours(grid, num_row, num_col):

#Get Rondom Cell Coordinate
def getRandomCell(grid):
    grid_size = grid
    #gridsize = len(grid)
    a = random.randint(0, grid_size - 1)
    b = random.randint(0, grid_size - 1)
    return (a, b)

def playGame():
    grid_size = 10
    number_of_mines = 4
    start = 0
    grid = setUpGrid(grid_size, start, number_of_mines)
    displayGrid(grid)

playGame()

