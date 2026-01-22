from collections import deque
import  random
from pydantic import BaseModel


class Cell(BaseModel):
    north: int = 1
    east: int = 1
    west: int = 1
    south: int = 1
    visited: bool = False
    distance: int = -1
    last: int = -1


width = 30
hight = 25
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

fd = open("output.txt", "w")
for index,row in enumerate(matrix):
    hex_list = []
    for cell in row:
        lst = []
        binary = ""
        lst.append(str(cell.west))
        lst.append(str(cell.south))
        lst.append(str(cell.east))
        lst.append(str(cell.north))
        binary = "".join(lst)
        decimal = int(binary, 2)
        hexadecimal = hex(decimal)[2:].upper()
        hex_list.append(hexadecimal)
    line = "".join(hex_list)
    if index == hight - 1:
        fd.write(f"{line}")
    else:
        fd.write(f"{line}\n")
fd.close





# binary_str = "1001"
# decimal = int(binary_str, 2)
# hex = hex(decimal)[2:]
# print(hex)