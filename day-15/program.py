from collections import defaultdict
from intcode import Runtime
import random

with open('input.txt') as input_file:
    lines = input_file.readlines()

line = lines[0]
program = list(map(int, line.split(",")))
runtime = Runtime(program[:])

pos = (0, 0)

dirs = {
    1: (0, -1),
    2: (0, 1),
    3: (-1, 0),
    4: (1, 0)
}


def add_tuple(a, b):
    return a[0] + b[0], a[1] + b[1]


movement = []

board = defaultdict(lambda: ' ')
board[(0, 0)] = '!'
moves = defaultdict(lambda: 1e10)
moves[pos] = 0
distance = moves[pos]
i = 0
exit = None
while True:
    while True:
        dir = random.choice(list(dirs.keys()))
        next_pos = add_tuple(pos, dirs[dir])
        if board[next_pos] != '#':
            break

    distance = moves[pos]
    runtime.inputs.append(dir)
    runtime.run()
    output = runtime.outputs.pop()

    if output == 0:
        wall_pos = add_tuple(pos, dirs[dir])
        board[wall_pos] = '#'
    elif output == 1:
        pos = add_tuple(pos, dirs[dir])
        moves[pos] = min(moves[pos], distance + 1)
        if board[pos] != "!":
            board[pos] = ' '
    elif output == 2:
        pos = add_tuple(pos, dirs[dir])
        moves[pos] = min(moves[pos], distance + 1)
        board[pos] = '*'
        exit = pos
    i += 1
    if i % 5000 == 0:
        print(i)
    if i > 200000 and exit is not None:
        break

left = min(board, key=lambda x: x[0])[0]
right = max(board, key=lambda x: x[0])[0]
top = min(board, key=lambda x: x[1])[1]
bottom = max(board, key=lambda x: x[1])[1]

for y in range(top, bottom + 1):
    print(''.join(board[x, y] for x in range(left, right + 1)))


def bfs(board, start):
    queue = [(start, 0)]
    filled = set()
    for item in queue:
        pos, depth = item
        next_nodes = [
            add_tuple(pos, dirs[1]),
            add_tuple(pos, dirs[2]),
            add_tuple(pos, dirs[3]),
            add_tuple(pos, dirs[4]),
        ]
        for new_node in next_nodes:
            if board[new_node] == '#' or new_node in filled:
                continue
            else:
                board[new_node] = 'O'
                filled.add(new_node)
                queue.append((new_node, depth + 1))
        print(depth)


bfs(board, exit)
for y in range(top, bottom + 1):
    print(''.join(board[x, y] for x in range(left, right + 1)))
