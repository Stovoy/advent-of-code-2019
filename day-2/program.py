with open('input.txt') as input_file:
    lines = input_file.readlines()


def run_program(program, noun, verb):
    program[1] = noun
    program[2] = verb

    i = 0
    while i < len(program):
        opcode = program[i]
        if opcode == 1:
            i0 = program[i + 1]
            i1 = program[i + 2]
            dest = program[i + 3]
            program[dest] = program[i0] + program[i1]
        elif opcode == 2:
            i0 = program[i + 1]
            i1 = program[i + 2]
            dest = program[i + 3]
            program[dest] = program[i0] * program[i1]
        elif opcode == 99:
            break
        i += 4

    return program[0]


def find_noun_verb(program, desired_output):
    for noun in range(0, 100):
        for verb in range(0, 100):
            result = run_program(program[:], noun, verb)
            if result == desired_output:
                return noun, verb


line = lines[0]
program = list(map(int, line.split(",")))
print(run_program(program[:], 12, 2))
noun, verb = find_noun_verb(program[:], 19690720)
print(100 * noun + verb)
