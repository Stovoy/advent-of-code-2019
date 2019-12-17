from advent import *

with open('input.txt') as input_file:
    lines = input_file.readlines()


program = parse_input_intcode(lines)

runtime = Runtime(program[:], [1])
runtime.run()
print(runtime.outputs[-1])

runtime = Runtime(program[:], [5])
runtime.run()
print(runtime.outputs[-1])
