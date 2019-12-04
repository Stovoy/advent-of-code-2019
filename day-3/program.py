with open('input.txt') as input_file:
    lines = input_file.readlines()


def run_wire(board, line):
    intersections = []
    x = 0
    y = 0
    center = (x, y)
    seen = set()
    steps = 0
    for coord in line.split(","):
        direction = coord[0]
        number = int(coord[1:])
        for i in range(number):
            if direction == 'R':
                x += 1
            elif direction == 'L':
                x -= 1
            elif direction == 'U':
                y += 1
            elif direction == 'D':
                y -= 1
            steps += 1
            position = x, y
            if position not in seen and position != center and position in board:
                intersections.append((x, y, steps + board[position]))
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
