from advent import *

with open('input.txt') as input_file:
    lines = input_file.readlines()

program =  parse_input_intcode(lines)

inputs = list(permutations(range(0, 5)))

outputs = []
for perm in inputs:
    amps = []
    for i in range(5):
        inputs = [perm[i]]
        if i == 0:
            inputs.append(0)
        amps.append(Runtime(program[:], inputs))

    for i in range(5):
        if i < 4:
            amps[i].add_output_runtime(amps[i + 1])
        if i > 0:
            amps[i].add_input_runtime(amps[i - 1])

    for amp in amps:
        amp.run()

    outputs.extend(amps[-1].outputs)
print(max(list(outputs)))

inputs = list(permutations(range(5, 10)))

outputs = []
for perm in inputs:
    amps = []
    for i in range(5):
        inputs = [perm[i]]
        if i == 0:
            inputs.append(0)
        amps.append(Runtime(program[:], inputs))

    for i in range(5):
        if i < 4:
            amps[i].add_output_runtime(amps[i + 1])
        else:
            amps[i].add_output_runtime(amps[0])
        if i > 0:
            amps[i].add_input_runtime(amps[i - 1])
        else:
            amps[i].add_input_runtime(amps[-1])

    for amp in amps:
        amp.run()

    outputs.extend(amps[-1].outputs)

print(max(list(outputs)))
