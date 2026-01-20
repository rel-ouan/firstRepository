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


def print__42(matrix, mat_42, width, hight):
    f1 = int(width / 2) - int(7 / 2)
    f2 = int(hight / 2) - int(5 / 2)
    for r_index, row in enumerate(matrix):
        for c_index, cell in enumerate(row):
            if r_index == f2 and c_index == f1:
                for c_index42, c in enumerate(mat_42[r_index ]):
                    matrix[r_index][c_index42] = c
    # return (matrix)


def main(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()

    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_BLACK)  # start
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)      # goal
    curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)      # goal
    
    start = (0, 0)
    exit = (1, 1)
    while True:
        width = 9
        hight = 7
        matrix = deque(
        deque(Cell() for i in range(width))
        for _ in range(hight)
        )
        key = stdscr.getkey()
        if key == "u":
            for row_index, row in enumerate(matrix):
                for col_index, cell in enumerate(row):
                    if row_index == 0 and col_index == width - 1:
                        cell.last = 1
                        # cell.visited = True
                    elif col_index == width - 1:
                        cell.north = 0
                        matrix[row_index - 1][col_index].south = 0
                        # cell.visited = True
                    elif row_index == 0:
                        cell.east = 0
                        matrix[row_index][col_index + 1].west = 0
                        # cell.visited = True
                    else:
                        flip_coin = random.choice([0, 1])
                        if flip_coin == 0:
                            cell.north = 0
                            matrix[row_index - 1][col_index].south = 0
                            # cell.visited = True
                        else:
                            cell.east = 0
                            matrix[row_index][col_index + 1].west = 0
                            # cell.visited = True
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
            stdscr.clear()
            closed = Cell()
            opened = Cell(north=0, east=0, west=0, south=0)
            d1 = [closed, Cell(north=0, east=0, west=1, south=0),
                opened, Cell(north=0, east=1, west=0, south=0),
                closed, closed, closed]
            d2 = [closed, Cell(north=0, east=0, west=1, south=0),
                opened, opened,
                Cell(north=1, east=0, west=0, south=1),
                Cell(north=1, east=1, west=0, south=1), closed]
            d3 = [closed, closed, closed, 
                Cell(north=0, east=1, west=1, south=0),
                closed, closed, closed]
            d4 = [Cell(north=1, east=0, west=0, south=0),
                Cell(north=1, east=1, west=0, south=0),
                closed, Cell(north=0, east=1, west=1, south=0),
                closed, Cell(north=1, east=0, west=1, south=1),
                Cell(north=1, east=0, west=0, south=1)]
            d5 = [opened, Cell(north=0, east=1, west=0, south=0),
                closed, Cell(north=0, east=1, west=1, south=0),
                closed, closed, closed]
            mat42 = deque([d1, d2, d3, d4, d5])
            matrix  = print__42(matrix, mat42, 9, 7)
            for y, row in enumerate(matrix):
                for x, cell in enumerate(row):
                    if cell.north == 1:
                        if x == width - 1:
                            n = "████"
                            stdscr.attron(curses.color_pair(1))
                            stdscr.addstr(y * 2, x * 3, n)
                            stdscr.attroff(curses.color_pair(1))
                        else:
                            n = "███"
                            stdscr.attron(curses.color_pair(1))
                            stdscr.addstr(y * 2, x * 3, n)
                            stdscr.attroff(curses.color_pair(1))
                    else:
                        stdscr.attron(curses.color_pair(1))
                        stdscr.addstr(y * 2, x * 3, "█  ")
                        stdscr.attroff(curses.color_pair(1))
                    if cell.west == 1:
                        stdscr.attron(curses.color_pair(1))
                        stdscr.addstr((y * 2) + 1, x * 3, "█")
                        stdscr.attroff(curses.color_pair(1))
                    else:
                        stdscr.attron(curses.color_pair(1))
                        stdscr.addstr((y * 2) + 1, x * 3, " ")
                        stdscr.attroff(curses.color_pair(1))
                    if cell.east == 1:
                        stdscr.attron(curses.color_pair(1))
                        stdscr.addstr((y * 2) + 1, (x * 3) + 3, "█")
                        stdscr.attroff(curses.color_pair(1))
                    else:
                        stdscr.attron(curses.color_pair(1))
                        stdscr.addstr((y * 2) + 1, (x * 3) + 3, " ")
                        stdscr.attroff(curses.color_pair(1))
                    if cell.south == 1:
                        if x == width - 1:
                            n = "████"
                            stdscr.attron(curses.color_pair(1))
                            stdscr.addstr((y * 2) + 2, x * 3, n)
                            stdscr.attroff(curses.color_pair(1))
                        else:
                            n = "███"
                            stdscr.attron(curses.color_pair(1))
                            stdscr.addstr((y * 2) + 2, x * 3, n)
                            stdscr.attroff(curses.color_pair(1))
                    else:
                        stdscr.attron(curses.color_pair(1))
                        stdscr.addstr((y * 2) + 2, x * 3, "████")
                        stdscr.attroff(curses.color_pair(1))
            # y_s, x_s = start 
            # stdscr.attron(curses.color_pair(2))
            # stdscr.addstr((y_s * 2) + 1, (x_s * 3) + 1, "██")
            # stdscr.attroff(curses.color_pair(2))
            # y_e, x_e = exit
            # stdscr.attron(curses.color_pair(3))
            # stdscr.addstr((y_e * 2) + 1, (x_e * 3) + 1, "██")
            # stdscr.attroff(curses.color_pair(3))
            # width_42 = 7
            # hight_42 = 5
            # matrix = []
            # closed = Cell()
            # opened = Cell(north=0, east=0, west=0, south=0)
            # d1 = [closed, Cell(north=0, east=0, west=1, south=0),
            #     opened, Cell(north=0, east=1, west=0, south=0),
            #     closed, closed, closed]
            # d2 = [closed, Cell(north=0, east=0, west=1, south=0),
            #     opened, opened,
            #     Cell(north=1, east=0, west=0, south=1),
            #     Cell(north=1, east=1, west=0, south=1), closed]
            # d3 = [closed, closed, closed, 
            #     Cell(north=0, east=1, west=1, south=0),
            #     closed, closed, closed]
            # d4 = [Cell(north=1, east=0, west=0, south=0),
            #     Cell(north=1, east=1, west=0, south=0),
            #     closed, Cell(north=0, east=1, west=1, south=0),
            #     closed, Cell(north=1, east=0, west=1, south=1),
            #     Cell(north=1, east=0, west=0, south=1)]
            # d5 = [opened, Cell(north=0, east=1, west=0, south=0),
            #     closed, Cell(north=0, east=1, west=1, south=0),
            #     closed, closed, closed]
            # mat42 = deque([d1, d2, d3, d4, d5])
            # # matrix.append(d1)
            # # matrix.append(d2)
            # # matrix.append(d3)
            # # matrix.append(d4)
            # # matrix.append(d5)
            # for y, row in enumerate(mat42):
            #     y += int(hight / 2) - int(hight_42 / 2)
            #     for x, cell in enumerate(row):
            #         x += int(width / 2) - int(width_42 / 2)
            #         if cell.north == 1:
            #             if x == width - 1:
            #                 n = "████"
            #                 stdscr.attron(curses.color_pair(1))
            #                 stdscr.addstr(y * 2, x * 3, n)
            #                 stdscr.attroff(curses.color_pair(1))
            #             else:
            #                 n = "████"
            #                 stdscr.attron(curses.color_pair(1))
            #                 stdscr.addstr(y * 2, x * 3, n)
            #                 stdscr.attroff(curses.color_pair(1))
            #         else:
            #             stdscr.attron(curses.color_pair(1))
            #             stdscr.addstr(y * 2, x * 3, "█  ")
            #             stdscr.attroff(curses.color_pair(1))
            #         if cell.west == 1:
            #             stdscr.attron(curses.color_pair(1))
            #             stdscr.addstr((y * 2) + 1, x * 3, "█")
            #             stdscr.attroff(curses.color_pair(1))
            #         else:
            #             stdscr.attron(curses.color_pair(1))
            #             stdscr.addstr((y * 2) + 1, x * 3, " ")
            #             stdscr.attroff(curses.color_pair(1))
            #         if cell.east == 1:
            #             stdscr.attron(curses.color_pair(1))
            #             stdscr.addstr((y * 2) + 1, (x * 3) + 3, "█")
            #             stdscr.attroff(curses.color_pair(1))
            #         else:
            #             stdscr.attron(curses.color_pair(1))
            #             stdscr.addstr((y * 2) + 1, (x * 3) + 3, " ")
            #             stdscr.attroff(curses.color_pair(1))
            #         if cell.south == 1:
            #             if x == width - 1:
            #                 n = "████"
            #                 stdscr.attron(curses.color_pair(1))
            #                 stdscr.addstr((y * 2) + 2, x * 3, n)
            #                 stdscr.attroff(curses.color_pair(1))
            #             else:
            #                 n = "███"
            #                 stdscr.attron(curses.color_pair(1))
            #                 stdscr.addstr((y * 2) + 2, x * 3, n)
            #                 stdscr.attroff(curses.color_pair(1))
            #         else:
            #             stdscr.attron(curses.color_pair(1))
            #             stdscr.addstr((y * 2) + 2, x * 3, "████")
            #             stdscr.attroff(curses.color_pair(1))
            # stdscr.refresh()
            # time.sleep(0.5)
        elif key == "e":
            break
    # stdscr.getch()

curses.wrapper(main)
