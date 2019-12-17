from advent import *

with open('input.txt') as input_file:
    lines = input_file.readlines()

result = 0
program = parse_input_intcode(lines)

runtime = Runtime(program[:], [1])
runtime.run()

print(runtime.outputs[0])

runtime = Runtime(program[:], [2])
runtime.run()

print(runtime.outputs[0])
