from itertools import permutations

with open('input.txt') as input_file:
    lines = input_file.readlines()


def parse_opcode(opcode):
    return opcode[2] == "0", opcode[1] == "0", opcode[0] == "0", int(opcode[3:5])


def parse_param(program, index, is_positional):
    return program[program[index]] if is_positional else program[index]


def write_to(program, address, value):
    program[address] = value


class Program:
    def __init__(self, program):
        self.program = program
        self.signals = []
        self.i = 0
        self.running = False
        self.write_to_amp = None
        self.outputs = []

    def run(self):
        write_to_amp = self.write_to_amp
        program = self.program
        i = self.i
        self.running = True
        while i < len(program):
            opcode = program[i]
            opcode = str(opcode)

            while len(opcode) < 5:
                opcode = "0" + opcode
            p0_positional, p1_positional, p2_positional, instruction = parse_opcode(opcode)
            if instruction == 1:
                p0 = parse_param(program, i + 1, p0_positional)
                p1 = parse_param(program, i + 2, p1_positional)
                write_to(program, program[i + 3], p0 + p1)
                i += 4
            elif instruction == 2:
                p0 = parse_param(program, i + 1, p0_positional)
                p1 = parse_param(program, i + 2, p1_positional)
                write_to(program, program[i + 3], p0 * p1)
                i += 4
            elif instruction == 3:
                if len(self.signals) == 0:
                    self.i = i
                    self.running = False
                    write_to_amp.unpause()
                    break
                write_to(program, program[i + 1], self.signals.pop(0))
                i += 2
            elif instruction == 4:
                p0 = parse_param(program, i + 1, p0_positional)
                write_to_amp.signals.append(p0)
                self.outputs.append(p0)
                i += 2
            elif instruction == 5:
                p0 = parse_param(program, i + 1, p0_positional)
                p1 = parse_param(program, i + 2, p1_positional)
                if p0 != 0:
                    i = p1
                else:
                    i += 3
            elif instruction == 6:
                p0 = parse_param(program, i + 1, p0_positional)
                p1 = parse_param(program, i + 2, p1_positional)
                if p0 == 0:
                    i = p1
                else:
                    i += 3
            elif instruction == 7:
                p0 = parse_param(program, i + 1, p0_positional)
                p1 = parse_param(program, i + 2, p1_positional)
                if p0 < p1:
                    write_to(program, program[i + 3], 1)
                else:
                    write_to(program, program[i + 3], 0)
                i += 4
            elif instruction == 8:
                p0 = parse_param(program, i + 1, p0_positional)
                p1 = parse_param(program, i + 2, p1_positional)
                if p0 == p1:
                    write_to(program, program[i + 3], 1)
                else:
                    write_to(program, program[i + 3], 0)
                i += 4
            elif instruction == 99:
                break
            else:
                raise ValueError(opcode)

    def unpause(self):
        self.run()

line = lines[0]
program = list(map(int, line.split(",")))

inputs = list(permutations(range(5, 10)))

max = 0
for perm in inputs:
    new_prog = program[:]
    amp_a = Program(new_prog[:])
    amp_b = Program(new_prog[:])
    amp_c = Program(new_prog[:])
    amp_d = Program(new_prog[:])
    amp_e = Program(new_prog[:])
    amp_a.signals.append(perm[0])
    amp_a.signals.append(0)
    amp_b.signals.append(perm[1])
    amp_c.signals.append(perm[2])
    amp_d.signals.append(perm[3])
    amp_e.signals.append(perm[4])
    amp_a.write_to_amp = amp_b
    amp_b.write_to_amp = amp_c
    amp_c.write_to_amp = amp_d
    amp_d.write_to_amp = amp_e
    amp_e.write_to_amp = amp_a
    amp_a.run()
    amp_b.run()
    amp_c.run()
    amp_d.run()
    amp_e.run()
    outputs = amp_e.outputs
    for output in outputs:
        if output > max:
            max = output
print(max)
