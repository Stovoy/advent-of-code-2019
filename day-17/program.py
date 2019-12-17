from advent import *

with open('input.txt') as input_file:
    lines = input_file.readlines()


def parse_board(outputs):
    x = 0
    y = 0
    board = defaultdict(lambda: ' ')
    for output in outputs:
        if output == 10:
            x = 0
            y += 1
        else:
            x += 1
            board[(x, y)] = str(chr(output))
    return board


line = lines[0]
program = list(map(int, line.split(",")))
runtime = Runtime(program[:])

runtime.run()

board = parse_board(runtime.outputs)
runtime.outputs = []

bounds = board_bounds(board)

robot_position = None
intersections = set()
scaffolds = set()
for x, y in iterate_board(board):
    if board[(x, y)] == '^':
        robot_position = (x, y)
    positions = [
        (x, y),
        (x + 1, y),
        (x - 1, y),
        (x, y + 1),
        (x, y - 1),
    ]
    if board[(x, y)] == '#':
        scaffolds.add((x, y))
    is_intersection = True
    for position in positions:
        if position in board and board[position] != '#':
            is_intersection = False
            break
    if is_intersection:
        intersections.add((x, y))

alignment_sum = 0
for intersection in intersections:
    x, y = intersection
    alignment = (x - bounds.left) * (y - bounds.top)
    alignment_sum += alignment
print(alignment_sum)


class RobotMovement:
    def __init__(self):
        self.position = 0
        self.direction = 0
        self.direction_index = up_index

        self.moved = 0
        self.travelled = set()
        self.intersection_directions_travelled = defaultdict(lambda: set())

    def move(self, position, direction_index):
        self.position = position
        self.direction = directions[direction_index]
        self.direction_index = direction_index

        self.moved = 0
        self.intersection_directions_travelled.clear()
        self.travelled.clear()

        instructions = []

        while len(self.travelled) < len(scaffolds):
            if tuple_add(self.position, self.direction) not in scaffolds:
                right_direction_index = (self.direction_index + 1) % 4
                left_direction_index = (self.direction_index - 1) % 4
                if tuple_add(self.position, directions[right_direction_index]) in scaffolds:
                    self.direction_index = right_direction_index
                    instructions += self.encode_moves() + ['R']
                else:
                    self.direction_index = left_direction_index
                    instructions += self.encode_moves() + ['L']
                self.direction = directions[self.direction_index]
            else:
                self.move_forward()

        return instructions + self.encode_moves()

    def encode_moves(self):
        instructions = []
        if self.moved > 0:
            instructions = [str(self.moved)]
            self.moved = 0
        return instructions

    def move_forward(self):
        self.moved += 1
        self.intersection_directions_travelled[self.position].add(self.direction_index)
        self.position = tuple_add(self.position, self.direction)
        self.travelled.add(self.position)


direction_index = 0

robot_movement = RobotMovement()
instructions = robot_movement.move(robot_position, direction_index)


def all_repeated_substr(str):
    repeated_strings = []
    search_strings = set()
    for i in range(len(str)):
        for j in range(i, len(str)):
            if len(str[i:j]) > 20:
                continue
            if str[i:j] == '' or str[i:j] == ',' or str[i:j][0] == ',' or str[i:j][-1] == ',':
                continue
            search_strings.add(str[i:j])
    for search in search_strings:
        repeated = [i for i in range(len(str)) if str.startswith(search, i)]
        if len(repeated) > 1:
            repeated_strings.append((search, repeated))
    return sorted(repeated_strings, key=lambda s: len(s[0]) * len(s[1]), reverse=True)


instructions = ','.join(instructions)
repeated_strings = all_repeated_substr(instructions)

valid = None
for a, b, c in combinations(repeated_strings, 3):
    indicies = []
    for repeat in [a, b, c]:
        for index in repeat[1]:
            indicies.append((index, index + len(repeat[0]) - 1))
    indicies = sorted(indicies, key=lambda i: i[0])
    if indicies[0][0] == 0 and indicies[-1][1] == len(instructions) - 1:
        is_valid = True
        for i in range(len(indicies) - 1):
            if indicies[i][1] != indicies[i + 1][0] - 2:
                is_valid = False
                break
        if is_valid:
            valid = a, b, c
            break

repeated_index_groups = [[(i, index) for index in repeated_string[1]]
                         for i, repeated_string in enumerate(valid)]
repeated_index_groups = sum(repeated_index_groups, [])
repeated_index_groups = sorted(repeated_index_groups, key=lambda index_group: index_group[1])
main_function = ','.join([chr(ord('A') + index_group[0]) for index_group in repeated_index_groups])

program[0] = 2
input_program = f'{main_function}\n' \
                f'{valid[0][0]}\n' \
                f'{valid[1][0]}\n' \
                f'{valid[2][0]}\n' \
                'n\n'

runtime = Runtime(program[:], list(map(ord, list(input_program))))
runtime.run()

frame = []
for i in range(len(runtime.outputs)):
    frame.append(runtime.outputs[i])
    if i > 0 and runtime.outputs[i - 1] == 10 and runtime.outputs[i] == 10:
        print('============================================================')
        print_board(parse_board(frame))
        frame.clear()

print(runtime.outputs[-1])
