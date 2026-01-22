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
    x_s = int(width / 2) - int(7 / 2)
    y_s = int(hight / 2) - int(5 / 2)
    start = (0, 0)
    exit = (14, 19)
    matrix = deque(
        deque(Cell() for i in range(width))
        for _ in range(hight)
    )
    close = [
            (y_s, x_s), (y_s, x_s + 4), (y_s, x_s + 5), (y_s, x_s + 6),
            (y_s + 1, x_s), (y_s + 1, x_s + 6), (y_s + 2, x_s), (y_s + 2, x_s + 1),
            (y_s + 2, x_s +  2), (y_s + 2, x_s + 4), (y_s + 2, x_s + 5), (y_s + 2, x_s + 6),
            (y_s + 3, x_s + 2), (y_s + 3, x_s + 4), (y_s + 4, x_s + 2), (y_s + 4, x_s + 4),
            (y_s + 4, x_s + 5), (y_s + 4, x_s + 6)
        ]
    open_north = [
        (y_s, x_s - 1), (y_s + 1, x_s - 1), (y_s + 2, x_s - 1),
        (y_s, x_s + 3), (y_s + 4, x_s + 1), (y_s + 2, x_s + 3),
        (y_s + 3, x_s + 3), (y_s + 4, x_s + 3), (y_s + 3, x_s - 1),
        (y_s + 1, x_s + 3), (y_s + 5, x_s + 1)
    ]
    open_east = [
        (y_s + 3, x_s), (y_s + 3, x_s + 5),  (y_s + 3, x_s + 6), (y_s + 5, x_s + 4),
        (y_s + 5, x_s + 5), (y_s + 5, x_s + 6), (y_s + 5, x_s + 4),
        (y_s + 1, x_s + 3), (y_s + 1, x_s + 4), (y_s + 5, x_s + 3),
        (y_s + 4, x_s - 1), (y_s + 3, x_s - 1), (y_s + 5, x_s + 2)
    ]
    open_west = [
        (y_s + 3, x_s + 1), (y_s + 1, x_s + 5)
    ]
    for tuple in close:
        y, x = tuple
        matrix[y][x].visited = True
    for tuple in open_north:
        y, x = tuple
        matrix[y][x].north = 0
        matrix[y][x].visited = True
        matrix[y - 1][x].south = 0
    for tuple in open_east:
        y, x = tuple
        matrix[y][x].east = 0
        matrix[y][x].visited = True
        matrix[y][x + 1].west = 0
    for tuple in open_west:
        y, x = tuple
        # matrix[y][x].west = 0
        matrix[y][x].visited = True
        # matrix[y][x - 1].east = 0
    for row_index, row in enumerate(matrix):
        for col_index, cell in enumerate(row):
            if row_index == 0 and col_index == width - 1 and cell.visited is False:
                cell.last = 1
                # cell.visited = True
            elif col_index == width - 1 and cell.visited is False:
                cell.north = 0
                # if matrix[row_index - 1][col_index].visited is False:
                matrix[row_index - 1][col_index].south = 0
                # cell.visited = True
            elif row_index == 0 and cell.visited is False:
                cell.east = 0
                # if matrix[row_index][col_index + 1].visited is False:
                matrix[row_index][col_index + 1].west = 0
                # cell.visited = True
            elif cell.visited is False:
                flip_coin = random.choice([0, 1])
                if flip_coin == 0:
                    cell.north = 0
                    # if matrix[row_index - 1][col_index].visited is False:
                    matrix[row_index - 1][col_index].south = 0
                    # cell.visited = True
                elif flip_coin == 1:
                    cell.east = 0
                    # if matrix[row_index][col_index + 1].visited is False: 
                    matrix[row_index][col_index + 1].west = 0
    for tuple in open_north:
        y, x = tuple
        matrix[y][x].visited = False
    for tuple in open_east:
        y, x = tuple
        matrix[y][x].visited = False
    for tuple in open_west:
        y, x = tuple
        matrix[y][x].visited = False
    # for row in matrix:
    #     for cell in row:
    #         print(cell)
    temp = copy.deepcopy(matrix)
    while check_matrix(temp) == False:
        y, x = exit
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
    for row in matrix:
        for cell in row:
            print(cell)
    y, x = start
    y_s, x_s = exit
    solution: list[str] = [] 
    while x != x_s or y != y_s:
        if matrix[y][x].east == 0 and matrix[y][x].distance - 1 == matrix[y][x + 1].distance:
            x += 1
            if x == x_s and y == y_s:
                break 
            print("e")
            solution.append("e")
        if matrix[y][x].west == 0 and matrix[y][x].distance - 1 == matrix[y][x - 1].distance:
            x -= 1
            if x == x_s and y == y_s:
                break 
            print("w")
            solution.append("w")
        if matrix[y][x].north == 0 and matrix[y][x].distance - 1 == matrix[y - 1][x].distance:
            y -= 1
            if x == x_s and y == y_s:
                break 
            print("n")
            solution.append("n")
        if matrix[y][x].south == 0 and matrix[y][x].distance - 1 == matrix[y + 1][x].distance:
            y += 1
            if x == x_s and y == y_s:
                break 
            print("s")
            solution.append("s")
        if x == x_s and y == y_s:
                break
    print(solution)


main()