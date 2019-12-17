from advent import *

with open('input.txt') as input_file:
    lines = input_file.readlines()

program = parse_input_intcode(lines)


def paint_panels(initial_state=None):
    panels = initial_state or {}
    panels = defaultdict(lambda: ' ', panels)
    pos = 0, 0
    dir_i = up_index
    runtime = Runtime(program[:])

    done = False
    while not done:
        runtime.inputs.append(0 if not panels[pos] else 1)
        runtime.outputs = []
        done = runtime.run()
        paint_white, turn_right = runtime.outputs
        panels[pos] = '#' if paint_white else ' '
        dir_i = direction_right(dir_i) if turn_right else direction_left(dir_i)
        pos = tuple_add(pos, directions[dir_i])

    return panels


panels = paint_panels()
print(len(panels))

panels = paint_panels({(0, 0): True})
white_panels = [panel for panel in panels.keys() if panels[panel]]
print_board(panels)
