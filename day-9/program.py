from intcode import Runtime


with open('input.txt') as input_file:
    lines = input_file.readlines()

result = 0
line = lines[0]
program = list(map(int, line.split(",")))

runtime = Runtime(program[:], [1])
runtime.run()

print(runtime.outputs[0])

runtime = Runtime(program[:], [2])
runtime.run()

print(runtime.outputs[0])
