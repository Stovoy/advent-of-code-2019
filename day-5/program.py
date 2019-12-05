with open('input.txt') as input_file:
    lines = input_file.readlines()


def parse_opcode(opcode):
    return opcode[2] == "0", opcode[1] == "0", opcode[0] == "0", int(opcode[3:5])


def parse_param(program, index, is_positional):
    return program[program[index]] if is_positional else program[index]


def write_to(program, address, value):
    program[address] = value


def run_program(program, input_value):
    i = 0
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
            write_to(program, program[i + 1], input_value)
            i += 2
        elif instruction == 4:
            p0 = parse_param(program, i + 1, p0_positional)
            print(p0)
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


line = lines[0]
program = list(map(int, line.split(",")))
run_program(program[:], 1)
run_program(program[:], 5)
