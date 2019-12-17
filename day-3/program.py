from advent import *

with open('input.txt') as input_file:
    lines = input_file.readlines()


def run_wire(board, line):
    intersections = []
    position = 0, 0
    center = position
    seen = set()
    steps = 0
    for coord in line.split(","):
        direction = coord[0]
        number = int(coord[1:])
        for i in range(number):
            if direction == 'R':
                position = tuple_add(position, right_dx)
            elif direction == 'L':
                position = tuple_add(position, left_dx)
            elif direction == 'U':
                position = tuple_add(position, up_dx)
            elif direction == 'D':
                position = tuple_add(position, down_dx)
            steps += 1
            if position not in seen and position != center and position in board:
                intersections.append((position[0], position[1], steps + board[position]))
            board[position] = steps
            seen.add(position)

    return intersections


board = {}

intersections = []
for line in lines:
    intersections += run_wire(board, line)

min_distance = min(abs(intersection[0]) + abs(intersection[1]) for intersection in intersections)
print(min_distance)

min_steps = min(intersection[2] for intersection in intersections)
print(min_steps)
