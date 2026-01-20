from curses import wrapper
from curses.textpad import Textbox, rectangle
from collections import deque
import curses
from pydantic import BaseModel
import random
import time
import copy


class Cell(BaseModel):
    north: int = 1
    east: int = 1
    west: int = 1
    south: int = 1
    visited: bool = False
    distance: int = -1
    last: int = -1

def check_matrix(matrix):
    for row in matrix:
        for cell in row:
            if cell.visited == False:
                return (False)
    return (True)


def main():
    width = 3
    hight = 3
    matrix = deque(
        deque(Cell() for i in range(width))
        for _ in range(hight)
    )
    for row_index, row in enumerate(matrix):
        for col_index, cell in enumerate(row):
            if row_index == 0 and col_index == width - 1:
                cell.last = 1
            elif col_index == width - 1:
                cell.north = 0
                matrix[row_index - 1][col_index].south = 0
            elif row_index == 0:
                cell.east = 0
                matrix[row_index][col_index + 1].west = 0
            else:
                flip_coin = random.choice([0, 1])
                if flip_coin == 0:
                    cell.north = 0
                    matrix[row_index - 1][col_index].south = 0
                else:
                    cell.east = 0
                    matrix[row_index][col_index + 1].west = 0
    for row in matrix:
        for cell in row:
            print(cell)
    temp = copy.deepcopy(matrix)
    while check_matrix(temp) == False:
        y = 2
        x = 2
        count = 0
        while True:
            if temp[y][x].north == 0:
                print("n")
                temp[y][x].visited = True
                temp[y][x].distance = count
                y -= 1
                temp[y][x].south = 1
                count += 1
                if temp[y][x].south == 1 and temp[y][x].west == 1 and temp[y][x].east == 1 and temp[y][x].north == 1:
                    print("0")
                    temp[y][x].visited = True
                    temp[y][x].distance = count
                    temp[y + 1][x].north = 1
                    break
            if temp[y][x].east == 0:
                print("e")
                temp[y][x].visited = True
                temp[y][x].distance = count
                x += 1
                temp[y][x].west = 1
                count += 1
                if temp[y][x].south == 1 and temp[y][x].north == 1 and temp[y][x].east == 1:
                    temp[y][x].visited = True
                    temp[y][x].distance = count
                    temp[y][x].west = 1
                    temp[y][x - 1].east = 1                                                            
                    break
            if temp[y][x].west == 0:
                print("w")
                temp[y][x].visited = True
                temp[y][x].distance = count
                x -= 1
                temp[y][x].east = 1
                count += 1
                if temp[y][x].south == 1 and temp[y][x].north == 1 and temp[y][x].west == 1:
                    temp[y][x].visited = True
                    temp[y][x].distance = count
                    temp[y][x + 1].west = 1
                    break
            if temp[y][x].south == 0:
                print("s")
                temp[y][x].visited = True
                temp[y][x].distance = count
                y += 1
                temp[y][x].north = 1
                count += 1
                if temp[y][x].south == 1 and temp[y][x].east == 1 and temp[y][x].west == 1:
                    temp[y][x].visited = True
                    temp[y][x].distance = count
                    temp[y - 1][x].south = 1
                    break
            if temp[y][x].north == 1 and temp[y][x].east == 1 and temp[y][x].west == 1 and temp[y][x].south == 1:
                print("1")
                break
            if check_matrix(temp) == True:
                print("2")
                break
        for row in temp:
            for cell in row:
                print(cell)
    
main()