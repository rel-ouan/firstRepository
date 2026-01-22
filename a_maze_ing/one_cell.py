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


def main(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()
    
    curses.init_color(9, 500, 500, 500)
    curses.init_pair(7, 9, curses.COLOR_BLACK)
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_BLACK)  # start
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)      # goal
    curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_BLACK)
    # stdscr.nodelay(True)
    index: int = 0
    width = 35
    hight = 30
    start = (5, 20)
    exit = (24, 0)
    x_s = int(width / 2) - int(7 / 2)
    y_s = int(hight / 2) - int(5 / 2)
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
    while True:
        # try:
        key = stdscr.getkey()
        # except:
        #     key = "1"
        matrix = deque(
                deque(Cell() for i in range(width))
                for _ in range(hight)
            )
        if key == "1":
            index = 0
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
                matrix[y][x].visited = True
            for row_index, row in enumerate(matrix):
                for col_index, cell in enumerate(row):
                    if row_index == 0 and col_index == width - 1 and cell.visited is False:
                        cell.last = 1
                    elif col_index == width - 1 and cell.visited is False:
                        cell.north = 0
                        matrix[row_index - 1][col_index].south = 0
                    elif row_index == 0 and cell.visited is False:
                        cell.east = 0
                        matrix[row_index][col_index + 1].west = 0
                    elif cell.visited is False:
                        flip_coin = random.choice([0, 1])
                        if flip_coin == 0:
                            cell.north = 0
                            matrix[row_index - 1][col_index].south = 0
                        elif flip_coin == 1:
                            cell.east = 0
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
            temp = copy.deepcopy(matrix)
            temp2 = copy.deepcopy(matrix)
            mat2 = copy.deepcopy(matrix)
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
            mat = copy.deepcopy(matrix)
            stdscr.clear()
            for y, row in enumerate(matrix):
                for x, cell in enumerate(row):
                    if cell.north == 1:
                        if x == width - 1:
                            n = "████"
                            stdscr.attron(curses.color_pair(1))
                            stdscr.addstr(y * 2, x * 3, n)
                            stdscr.attroff(curses.color_pair(1))
                            stdscr.refresh()
                            time.sleep(0.0008)
                        else:
                            n = "███"
                            stdscr.attron(curses.color_pair(1))
                            stdscr.addstr(y * 2, x * 3, n)
                            stdscr.attroff(curses.color_pair(1))
                            stdscr.refresh()
                            time.sleep(0.0008)
                    else:
                        stdscr.attron(curses.color_pair(1))
                        stdscr.addstr(y * 2, x * 3, "█  ")
                        stdscr.attroff(curses.color_pair(1))
                        stdscr.refresh()
                        time.sleep(0.0008)
                    if cell.west == 1:
                        stdscr.attron(curses.color_pair(1))
                        stdscr.addstr((y * 2) + 1, x * 3, "█")
                        stdscr.attroff(curses.color_pair(1))
                        stdscr.refresh()
                        time.sleep(0.0008)
                    else:
                        stdscr.attron(curses.color_pair(1))
                        stdscr.addstr((y * 2) + 1, x * 3, " ")
                        stdscr.attroff(curses.color_pair(1))
                        stdscr.refresh()
                        time.sleep(0.0008)
                    if cell.east == 1:
                        stdscr.attron(curses.color_pair(1))
                        stdscr.addstr((y * 2) + 1, (x * 3) + 3, "█")
                        stdscr.attroff(curses.color_pair(1))
                        stdscr.refresh()
                        time.sleep(0.0008)
                    else:
                        stdscr.attron(curses.color_pair(1))
                        stdscr.addstr((y * 2) + 1, (x * 3) + 3, " ")
                        stdscr.attroff(curses.color_pair(1))
                        stdscr.refresh()
                        time.sleep(0.0008)
                    if cell.south == 1:
                        if x == width - 1:
                            n = "████"
                            stdscr.attron(curses.color_pair(1))
                            stdscr.addstr((y * 2) + 2, x * 3, n)
                            stdscr.attroff(curses.color_pair(1))
                            stdscr.refresh()
                            time.sleep(0.0008)
                        else:
                            n = "███"
                            stdscr.attron(curses.color_pair(1))
                            stdscr.addstr((y * 2) + 2, x * 3, n)
                            stdscr.attroff(curses.color_pair(1))
                            stdscr.refresh()
                            time.sleep(0.0008)
                    else:
                        stdscr.attron(curses.color_pair(1))
                        stdscr.addstr((y * 2) + 2, x * 3, "█  █")
                        stdscr.attroff(curses.color_pair(1))
                        stdscr.refresh()
                        time.sleep(0.0008)
            for tuple in close:
                y, x = tuple
                stdscr.attron(curses.color_pair(7))
                stdscr.addstr((y * 2) + 1, (x * 3) + 1, "██")
                stdscr.attroff(curses.color_pair(7))
            y_e, x_e = exit
            y_s, x_s = start
            stdscr.attron(curses.color_pair(2))
            stdscr.addstr((y_s * 2) + 1, (x_s * 3) + 1, "██")
            stdscr.attroff(curses.color_pair(2))
            stdscr.attron(curses.color_pair(3))
            stdscr.addstr((y_e * 2) + 1, (x_e * 3) + 1, "██")
            stdscr.attroff(curses.color_pair(3))
            stdscr.refresh()
            time.sleep(0.5)
        elif key == "2":
            index += 1
            stdscr.clear()
            if index % 2  != 0:
                for y, row in enumerate(mat):
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
                            stdscr.addstr((y * 2) + 2, x * 3, "█  █")
                            stdscr.attroff(curses.color_pair(1))
                for tuple in close:
                    y, x = tuple
                    stdscr.attron(curses.color_pair(7))
                    stdscr.addstr((y * 2) + 1, (x * 3) + 1, "██")
                    stdscr.attroff(curses.color_pair(7))
                y_e, x_e = exit
                y_s, x_s = start
                stdscr.attron(curses.color_pair(2))
                stdscr.addstr((y_s * 2) + 1, (x_s * 3) + 1, "██")
                stdscr.attroff(curses.color_pair(2))
                stdscr.attron(curses.color_pair(3))
                stdscr.addstr((y_e * 2) + 1, (x_e * 3) + 1, "██")
                stdscr.attroff(curses.color_pair(3))
                # stdscr.refresh()
                # time.sleep(0.5)
                # elif key == "s":
                solution: list[str] = [] 
                while x_s != x_e or y_s != y_e:
                    if mat[y_s][x_s].east == 0 and mat[y_s][x_s].distance - 1 == mat[y_s][x_s + 1].distance:
                        x_s += 1
                        if x_s == x_e and y_s == y_e:
                            break
                        # if matrix[y][x].east == 1 or matrix[y][x].distance - 1 != matrix[y][x + 1].distance:
                        #     stdscr.attron(curses.color_pair(2))
                        #     stdscr.addstr((y * 2) + 1, (x * 3) + 1, "██")
                        #     stdscr.attroff(curses.color_pair(2))
                        # else:
                        stdscr.attron(curses.color_pair(4))
                        stdscr.addstr((y_s * 2) + 1, (x_s * 3), "█")
                        stdscr.addstr((y_s * 2) + 1, (x_s * 3) + 1, "██")
                        stdscr.attroff(curses.color_pair(4))
                        # print("e")
                        solution.append("e")
                    if mat[y_s][x_s].west == 0 and mat[y_s][x_s].distance - 1 == mat[y_s][x_s - 1].distance:
                        x_s -= 1
                        if x_s == x_e and y_s == y_e:
                            stdscr.attron(curses.color_pair(4))
                            stdscr.addstr((y_s * 2) + 1, (x_s * 3) + 3, "█")
                            stdscr.attron(curses.color_pair(4))
                            break
                        # if x == width - 1:
                        #     stdscr.attron(curses.color_pair(2))
                        #     stdscr.addstr((y * 2) + 1, (x * 3) + 1, "██")
                        #     stdscr.attroff(curses.color_pair(2))
                        # else:
                        stdscr.attron(curses.color_pair(4))
                        stdscr.addstr((y_s * 2) + 1, (x_s * 3) + 3, "█")
                        stdscr.addstr((y_s* 2) + 1, (x_s * 3) + 1, "██")
                        stdscr.attroff(curses.color_pair(4))
                        # print("w")
                        solution.append("w")
                    if mat[y_s][x_s].north == 0 and mat[y_s][x_s].distance - 1 == mat[y_s - 1][x_s].distance:
                        y_s -= 1
                        if x_s == x_e and y_s == y_e:
                            break
                        stdscr.attron(curses.color_pair(4))
                        stdscr.addstr((y_s  * 2) + 2, (x_s * 3) + 1, "██")                    
                        stdscr.addstr((y_s * 2) + 1, (x_s * 3) + 1, "██")
                        stdscr.attroff(curses.color_pair(4))
                        # print("n")
                        solution.append("n")
                    if mat[y_s][x_s].south == 0 and mat[y_s][x_s].distance - 1 == mat[y_s + 1][x_s].distance:
                        y_s += 1
                        if x_s == x_e and y_s == y_e:
                            stdscr.attron(curses.color_pair(4))    
                            stdscr.addstr((y_s * 2), (x_s * 3) + 1, "██")
                            stdscr.attroff(curses.color_pair(4))    
                            break
                        stdscr.attron(curses.color_pair(4))
                        stdscr.addstr((y_s * 2), (x_s * 3) + 1, "██")
                        stdscr.addstr((y_s * 2) + 1, (x_s * 3) + 1, "██")
                        stdscr.attroff(curses.color_pair(4))
                        # print("s")
                        solution.append("s")
                # for row_i, row in enumerate(matrix):
                #     for coll_i,cell in enumerate(row):
                #         stdscr.addstr((row_i * 2) + 1, (coll_i * 3) + 1, str(cell.distance))
                    stdscr.refresh()
                    time.sleep(0.08)
                    # stdscr.getch()
            elif index % 2 == 0:
                stdscr.clear()
                while check_matrix(temp2) == False:
                    y, x = start
                    count = 0
                    while True:
                        if temp2[y][x].north == 0:
                            # print("n")
                            temp2[y][x].visited = True
                            mat2[y][x].distance = count
                            y -= 1
                            temp2[y][x].south = 1
                            count += 1
                            if temp2[y][x].south == 1 and temp2[y][x].west == 1 and temp2[y][x].east == 1 and temp2[y][x].north == 1:
                                temp2[y][x].visited = True
                                mat2[y][x].distance = count
                                temp2[y + 1][x].north = 1
                                break
                        if temp2[y][x].east == 0:
                            # print("e")
                            temp2[y][x].visited = True
                            mat2[y][x].distance = count
                            x += 1
                            temp2[y][x].west = 1
                            count += 1
                            if temp2[y][x].south == 1 and temp2[y][x].north == 1 and temp2[y][x].east == 1:
                                temp2[y][x].visited = True
                                mat2[y][x].distance = count
                                temp2[y][x].west = 1
                                temp2[y][x - 1].east = 1                                                            
                                break
                        if temp2[y][x].west == 0:
                            # print("w")
                            temp2[y][x].visited = True
                            mat2[y][x].distance = count
                            x -= 1
                            temp2[y][x].east = 1
                            count += 1
                            if temp2[y][x].south == 1 and temp2[y][x].north == 1 and temp2[y][x].west == 1:
                                temp2[y][x].visited = True
                                mat2[y][x].distance = count
                                temp2[y][x + 1].west = 1
                                break
                        if temp2[y][x].south == 0:
                            # print("s")
                            temp2[y][x].visited = True
                            mat2[y][x].distance = count
                            y += 1
                            temp2[y][x].north = 1
                            count += 1
                            if temp2[y][x].south == 1 and temp2[y][x].east == 1 and temp2[y][x].west == 1:
                                temp2[y][x].visited = True
                                mat2[y][x].distance = count
                                temp2[y - 1][x].south = 1
                                break
                        if temp2[y][x].north == 1 and temp2[y][x].east == 1 and temp2[y][x].west == 1 and temp2[y][x].south == 1:
                            break
                        if check_matrix(temp2) == True:
                            break
                for y, row in enumerate(mat):
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
                            stdscr.addstr((y * 2) + 2, x * 3, "█  █")
                            stdscr.attroff(curses.color_pair(1))
                            stdscr.attroff(curses.color_pair(1))
                for tuple in close:
                    y, x = tuple
                    stdscr.attron(curses.color_pair(7))
                    stdscr.addstr((y * 2) + 1, (x * 3) + 1, "██")
                    stdscr.attroff(curses.color_pair(7))
                y_s, x_s = start
                y_e, x_e = exit
                stdscr.attron(curses.color_pair(2))
                stdscr.addstr((y_s * 2) + 1, (x_s * 3) + 1, "██")
                stdscr.attroff(curses.color_pair(2))
                stdscr.attron(curses.color_pair(3))
                stdscr.addstr((y_e * 2) + 1, (x_e * 3) + 1, "██")
                stdscr.attroff(curses.color_pair(3))
                stdscr.refresh()
                while x_s != x_e or y_s != y_e:
                    if mat[y_s][x_s].east == 0 and mat[y_s][x_s].distance - 1 == mat[y_s][x_s + 1].distance:
                        x_s += 1
                        if x_s == x_e and y_s == y_e:
                            break
                        # if matrix[y][x].east == 1 or matrix[y][x].distance - 1 != matrix[y][x + 1].distance:
                        #     stdscr.attron(curses.color_pair(2))
                        #     stdscr.addstr((y * 2) + 1, (x * 3) + 1, "██")
                        #     stdscr.attroff(curses.color_pair(2))
                        # else:
                        stdscr.attron(curses.color_pair(4))
                        stdscr.addstr((y_s * 2) + 1, (x_s * 3), "█")
                        stdscr.addstr((y_s * 2) + 1, (x_s * 3) + 1, "██")
                        stdscr.attroff(curses.color_pair(4))
                        # print("e")
                        solution.append("e")
                    if mat[y_s][x_s].west == 0 and mat[y_s][x_s].distance - 1 == mat[y_s][x_s - 1].distance:
                        x_s -= 1
                        if x_s == x_e and y_s == y_e:
                            stdscr.attron(curses.color_pair(4))
                            stdscr.addstr((y_s * 2) + 1, (x_s * 3) + 3, "█")
                            stdscr.attron(curses.color_pair(4))
                            break
                        # if x == width - 1:
                        #     stdscr.attron(curses.color_pair(2))
                        #     stdscr.addstr((y * 2) + 1, (x * 3) + 1, "██")
                        #     stdscr.attroff(curses.color_pair(2))
                        # else:
                        stdscr.attron(curses.color_pair(4))
                        stdscr.addstr((y_s * 2) + 1, (x_s * 3) + 3, "█")
                        stdscr.addstr((y_s* 2) + 1, (x_s * 3) + 1, "██")
                        stdscr.attroff(curses.color_pair(4))
                        # print("w")
                        solution.append("w")
                    if mat[y_s][x_s].north == 0 and mat[y_s][x_s].distance - 1 == mat[y_s - 1][x_s].distance:
                        y_s -= 1
                        if x_s == x_e and y_s == y_e:
                            break
                        stdscr.attron(curses.color_pair(4))
                        stdscr.addstr((y_s  * 2) + 2, (x_s * 3) + 1, "██")                    
                        stdscr.addstr((y_s * 2) + 1, (x_s * 3) + 1, "██")
                        stdscr.attroff(curses.color_pair(4))
                        # print("n")
                        solution.append("n")
                    if mat[y_s][x_s].south == 0 and mat[y_s][x_s].distance - 1 == mat[y_s + 1][x_s].distance:
                        y_s += 1
                        if x_s == x_e and y_s == y_e:
                            stdscr.attron(curses.color_pair(4))    
                            stdscr.addstr((y_s * 2), (x_s * 3) + 1, "██")
                            stdscr.attroff(curses.color_pair(4))    
                            break
                        stdscr.attron(curses.color_pair(4))
                        stdscr.addstr((y_s * 2), (x_s * 3) + 1, "██")
                        stdscr.addstr((y_s * 2) + 1, (x_s * 3) + 1, "██")
                        stdscr.attroff(curses.color_pair(4))
                        # print("s")
                        solution.append("s")
                # for row_i, row in enumerate(matrix):
                #     for coll_i,cell in enumerate(row):
                #         stdscr.addstr((row_i * 2) + 1, (coll_i * 3) + 1, str(cell.distance))
                    stdscr.refresh()
                    # time.sleep(0.1)
                # time.sleep(0.5)
                # elif key == "s":
                # solution: list[str] = [] 
                y_e, x_e = start
                y_s, x_s = exit
                while x_s != x_e or y_s != y_e:
                    if mat2[y_s][x_s].east == 0 and mat2[y_s][x_s].distance - 1 == mat2[y_s][x_s + 1].distance:
                        x_s += 1
                        if x_s == x_e and y_s == y_e:
                            stdscr.attron(curses.color_pair(5))
                            stdscr.addstr((y_s * 2) + 1, (x_s * 3), "█")
                            stdscr.attron(curses.color_pair(5))
                            break
                        # if matrix[y][x].east == 1 or matrix[y][x].distance - 1 != matrix[y][x + 1].distance:
                        #     stdscr.attron(curses.color_pair(2))
                        #     stdscr.addstr((y * 2) + 1, (x * 3) + 1, "██")
                        #     stdscr.attroff(curses.color_pair(2))
                        # else:
                        stdscr.attron(curses.color_pair(5))
                        stdscr.addstr((y_s * 2) + 1, (x_s * 3), "█")
                        stdscr.addstr((y_s * 2) + 1, (x_s * 3) + 1, "██")
                        stdscr.attroff(curses.color_pair(5))
                        # print("e")
                        # solution.append("e")
                    if mat2[y_s][x_s].west == 0 and mat2[y_s][x_s].distance - 1 == mat2[y_s][x_s - 1].distance:
                        x_s -= 1
                        if x_s == x_e and y_s == y_e:
                            stdscr.attron(curses.color_pair(5))
                            stdscr.addstr((y_s * 2) + 1, (x_s * 3) + 3, "█")
                            stdscr.attron(curses.color_pair(5))
                            break
                        # if x == width - 1:
                        #     stdscr.attron(curses.color_pair(2))
                        #     stdscr.addstr((y * 2) + 1, (x * 3) + 1, "██")
                        #     stdscr.attroff(curses.color_pair(2))
                        # else:
                        stdscr.attron(curses.color_pair(5))
                        stdscr.addstr((y_s * 2) + 1, (x_s * 3) + 3, "█")
                        stdscr.addstr((y_s* 2) + 1, (x_s * 3) + 1, "██")
                        stdscr.attroff(curses.color_pair(5))
                        # print("w")
                        # solution.append("w")
                    if mat2[y_s][x_s].north == 0 and mat2[y_s][x_s].distance - 1 == mat2[y_s - 1][x_s].distance:
                        y_s -= 1
                        if x_s == x_e and y_s == y_e:
                            stdscr.attron(curses.color_pair(5))
                            stdscr.addstr((y_s  * 2) + 2, (x_s * 3) + 1, "██")
                            stdscr.attroff(curses.color_pair(5))
                            break
                        stdscr.attron(curses.color_pair(5))
                        stdscr.addstr((y_s  * 2) + 2, (x_s * 3) + 1, "██")                    
                        stdscr.addstr((y_s * 2) + 1, (x_s * 3) + 1, "██")
                        stdscr.attroff(curses.color_pair(5))
                        # print("n")
                        # solution.append("n")
                    if mat2[y_s][x_s].south == 0 and mat2[y_s][x_s].distance - 1 == mat2[y_s + 1][x_s].distance:
                        y_s += 1
                        if x_s == x_e and y_s == y_e:
                            stdscr.attron(curses.color_pair(5))    
                            stdscr.addstr((y_s * 2), (x_s * 3) + 1, "██")
                            stdscr.attroff(curses.color_pair(5))    
                            break
                        stdscr.attron(curses.color_pair(5))
                        stdscr.addstr((y_s * 2), (x_s * 3) + 1, "██")
                        stdscr.addstr((y_s * 2) + 1, (x_s * 3) + 1, "██")
                        stdscr.attroff(curses.color_pair(5))
                        # print("s")
                        # solution.append("s")
                # for row_i, row in enumerate(matrix):
                #     for coll_i,cell in enumerate(row):
                #         stdscr.addstr((row_i * 2) + 1, (coll_i * 3) + 1, str(cell.distance))
                    stdscr.refresh()
                    time.sleep(0.010)
                    # stdscr.getch()
        elif key == "e":
            break
    stdscr.getch()


curses.wrapper(main)