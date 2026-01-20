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
    width = 20
    hight = 15
    start = (1, 1)
    exit = (12, 10)
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
        y, x = start
        count = 0
        while True:
            if temp[y][x].north == 0:
                # print("n")
                temp[y][x].visited = True
                matrix[y][x].distance = count
                y -= 1
                temp[y][x].south = 1
                count += 1
                if temp[y][x].south == 1 and temp[y][x].west == 1 and temp[y][x].east == 1 and temp[y][x].north == 1:
                    # print("0")
                    temp[y][x].visited = True
                    matrix[y][x].distance = count
                    temp[y + 1][x].north = 1
                    break
            if temp[y][x].east == 0:
                # print("e")
                temp[y][x].visited = True
                matrix[y][x].distance = count
                x += 1
                temp[y][x].west = 1
                count += 1
                if temp[y][x].south == 1 and temp[y][x].north == 1 and temp[y][x].east == 1:
                    temp[y][x].visited = True
                    matrix[y][x].distance = count
                    temp[y][x].west = 1
                    temp[y][x - 1].east = 1                                                            
                    break
            if temp[y][x].west == 0:
                # print("w")
                temp[y][x].visited = True
                matrix[y][x].distance = count
                x -= 1
                temp[y][x].east = 1
                count += 1
                if temp[y][x].south == 1 and temp[y][x].north == 1 and temp[y][x].west == 1:
                    temp[y][x].visited = True
                    matrix[y][x].distance = count
                    temp[y][x + 1].west = 1
                    break
            if temp[y][x].south == 0:
                # print("s")
                temp[y][x].visited = True
                matrix[y][x].distance = count
                y += 1
                temp[y][x].north = 1
                count += 1
                if temp[y][x].south == 1 and temp[y][x].east == 1 and temp[y][x].west == 1:
                    temp[y][x].visited = True
                    matrix[y][x].distance = count
                    temp[y - 1][x].south = 1
                    break
            if temp[y][x].north == 1 and temp[y][x].east == 1 and temp[y][x].west == 1 and temp[y][x].south == 1:
                break
            if check_matrix(temp) == True:
                break
        # for row in temp:
        #     for cell in row:
        #         print(cell)
    y, x = exit
    y_s, x_s = start
    solution: list[str] = [] 
    while x != x_s or y != y_s:
        if matrix[y][x].east == 0 and matrix[y][x].distance - 1 == matrix[y][x + 1].distance:
            x += 1
            print("e")
            solution.append("e")
        if matrix[y][x].west == 0 and matrix[y][x].distance - 1 == matrix[y][x - 1].distance:
            x -= 1
            print("w")
            solution.append("w")
        if matrix[y][x].north == 0 and matrix[y][x].distance - 1 == matrix[y - 1][x].distance:
            y -= 1
            print("n")
            solution.append("n")
        if matrix[y][x].south == 0 and matrix[y][x].distance - 1 == matrix[y + 1][x].distance:
            y + 1
            if x == x_s and y == y_s:
                break 
            print("s")
            solution.append("s")
    print(solution)


main()