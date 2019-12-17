from advent import *

with open('input.txt') as input_file:
    lines = input_file.readlines()

line = lines[0]
program = list(map(int, line.split(",")))
runtime = Runtime(program[:])

pos = (0, 0)

dirs = {
    1: up_dx,
    2: down_dx,
    3: left_dx,
    4: right_dx
}

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
        next_pos = tuple_add(pos, dirs[dir])
        if board[next_pos] != '#':
            break

    distance = moves[pos]
    runtime.inputs.append(dir)
    runtime.run()
    output = runtime.outputs.pop()

    if output == 0:
        wall_pos = tuple_add(pos, dirs[dir])
        board[wall_pos] = '#'
    elif output == 1:
        pos = tuple_add(pos, dirs[dir])
        moves[pos] = min(moves[pos], distance + 1)
        if board[pos] != "!":
            board[pos] = ' '
    elif output == 2:
        pos = tuple_add(pos, dirs[dir])
        moves[pos] = min(moves[pos], distance + 1)
        board[pos] = '*'
        exit = pos
    i += 1
    if i % 5000 == 0:
        print(i)
    if i > 200000 and exit is not None:
        break

print_board(board)


def bfs(board, start):
    queue = [(start, 0)]
    filled = set()
    for item in queue:
        pos, depth = item
        next_nodes = [
            tuple_add(pos, dirs[1]),
            tuple_add(pos, dirs[2]),
            tuple_add(pos, dirs[3]),
            tuple_add(pos, dirs[4]),
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
print_board(board)
