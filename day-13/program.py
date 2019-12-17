from advent import *

with open('input.txt') as input_file:
    lines = input_file.readlines()

line = lines[0]
program = list(map(int, line.split(",")))
runtime = Runtime(program[:])
runtime.run()

outputs = runtime.outputs

block_count = sum(1 for i in range(0, len(outputs), 3)
                  if runtime.outputs[i + 2] == 2)
print(block_count)

program[0] = 2
runtime = Runtime(program[:])

ball_x = 0
paddle_x = 0

while not runtime.run():
    outputs = runtime.outputs
    runtime.outputs = []

    for i in range(0, len(outputs), 3):
        x, y, type = outputs[i], outputs[i + 1], outputs[i + 2]

        if type == 3:
            paddle_x = x
        elif type == 4:
            ball_x = x

    if ball_x < paddle_x:
        runtime.inputs.append(-1)
    elif ball_x > paddle_x:
        runtime.inputs.append(1)
    else:
        runtime.inputs.append(0)

for i in range(0, len(runtime.outputs), 3):
    if runtime.outputs[i] == -1 and runtime.outputs[i + 1] == 0:
        print(runtime.outputs[i + 2])
