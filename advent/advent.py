import math


def tuple_add(a, b):
    return a[0] + b[0], a[1] + b[1]


def tuple_subtract(a, b):
    return a[0] - b[0], a[1] - b[1]


class Bounds:
    def __init__(self, left, right, top, bottom):
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom


def board_bounds(board):
    return Bounds(
        left=min(board, key=lambda x: x[0])[0],
        right=max(board, key=lambda x: x[0])[0],
        top=min(board, key=lambda x: x[1])[1],
        bottom=max(board, key=lambda x: x[1])[1])


def print_board(board):
    bounds = board_bounds(board)
    for y in range(bounds.top, bounds.bottom + 1):
        print(''.join(board[x, y] for x in range(bounds.left, bounds.right + 1)))


directions = [
    (0, -1),
    (1, 0),
    (0, 1),
    (-1, 0)
]

up_index, left_index, down_index, right_index = 0, 1, 2, 3
up_dx, left_dx, down_dx, right_dx = directions


def direction_right(direction_index):
    return (direction_index + 1) % 4


def direction_left(direction_index):
    return (direction_index - 1) % 4


def lcm(a, b):
    return (a * b) // math.gcd(a, b)


def parse_input_intcode(lines):
    return list(map(int, lines[0].split(",")))
