from intcode import Runtime

with open('input.txt') as input_file:
    lines = input_file.readlines()


def run_noun_verb(program, noun, verb):
    program = program[:]
    program[1] = noun
    program[2] = verb
    runtime = Runtime(program)
    runtime.run()
    return program[0]


def find_noun_verb(program, desired_output):
    for noun in range(0, 100):
        for verb in range(0, 100):
            if run_noun_verb(program, noun, verb) == desired_output:
                return noun, verb


line = lines[0]
program = list(map(int, line.split(",")))
print(run_noun_verb(program, 12, 2))
noun, verb = find_noun_verb(program, 19690720)
print(100 * noun + verb)
