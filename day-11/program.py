from intcode import Runtime
from collections import defaultdict

with open('input.txt') as input_file:
    lines = input_file.readlines()

line = lines[0]
program = list(map(int, line.split(",")))


def paint_panels(initial_state=None):
    panels = initial_state or {}
    panels = defaultdict(lambda: False, panels)
    pos = 0, 0
    dirs = [
        (0, -1),
        (-1, 0),
        (0, 1),
        (1, 0)
    ]
    dir_i = 0
    runtime = Runtime(program[:])

    done = False
    while not done:
        runtime.inputs.append(0 if not panels[pos] else 1)
        runtime.outputs = []
        done = runtime.run()
        paint_white, turn_right = runtime.outputs
        panels[pos] = paint_white
        dir_i += -1 if turn_right else 1
        dir_i %= 4
        pos = tuple(map(sum, zip(pos, dirs[dir_i])))

    return panels


panels = paint_panels()
print(len(panels))

panels = paint_panels({(0, 0): True})
white_panels = [panel for panel in panels.keys() if panels[panel]]
left = min(white_panels, key=lambda x: x[0])[0]
right = max(white_panels, key=lambda x: x[0])[0]
top = min(white_panels, key=lambda x: x[1])[1]
bottom = max(white_panels, key=lambda x: x[1])[1]

for y in range(top, bottom + 1):
    print(''.join('#' if panels[x, y] else ' ' for x in range(left, right + 1)))
