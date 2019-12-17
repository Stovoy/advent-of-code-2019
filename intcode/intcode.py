PARAM_0 = 1
PARAM_1 = 2
PARAM_2 = 3


class Flags:
    def __init__(self):
        self.is_positional = {
            PARAM_0: False,
            PARAM_1: False,
            PARAM_2: False,
        }
        self.is_relative = {
            PARAM_0: False,
            PARAM_1: False,
            PARAM_2: False,
        }


class Opcode:
    pass


class Add(Opcode):
    def process(self, runtime):
        p0 = runtime.parse_param(PARAM_0)
        p1 = runtime.parse_param(PARAM_1)
        runtime.write_param(PARAM_2, p0 + p1)
        runtime.i += 4


class Mul(Opcode):
    def process(self, runtime):
        p0 = runtime.parse_param(PARAM_0)
        p1 = runtime.parse_param(PARAM_1)
        runtime.write_param(PARAM_2, p0 * p1)
        runtime.i += 4


class Input(Opcode):
    def process(self, runtime):
        if len(runtime.inputs) == 0:
            runtime.run_input_runtimes()
            raise StopIteration
        runtime.write_param(PARAM_0, runtime.inputs.pop(0))
        runtime.i += 2


class Output(Opcode):
    def process(self, runtime):
        runtime.output(runtime.parse_param(PARAM_0))
        runtime.i += 2


class NotZero(Opcode):
    def process(self, runtime):
        p0 = runtime.parse_param(PARAM_0)
        p1 = runtime.parse_param(PARAM_1)
        if p0 != 0:
            runtime.i = p1
        else:
            runtime.i += 3


class Zero(Opcode):
    def process(self, runtime):
        p0 = runtime.parse_param(PARAM_0)
        p1 = runtime.parse_param(PARAM_1)
        if p0 == 0:
            runtime.i = p1
        else:
            runtime.i += 3


class LessThan(Opcode):
    def process(self, runtime):
        p0 = runtime.parse_param(PARAM_0)
        p1 = runtime.parse_param(PARAM_1)
        runtime.write_param(PARAM_2, int(p0 < p1))
        runtime.i += 4


class Equal(Opcode):
    def process(self, runtime):
        p0 = runtime.parse_param(PARAM_0)
        p1 = runtime.parse_param(PARAM_1)
        runtime.write_param(PARAM_2, int(p0 == p1))
        runtime.i += 4


class AdjustRelativeBase(Opcode):
    def process(self, runtime):
        runtime.relative_base += runtime.parse_param(PARAM_0)
        runtime.i += 2


class Exit(Opcode):
    def process(self, runtime):
        runtime.stop()


Opcodes = {
    1: Add(),
    2: Mul(),
    3: Input(),
    4: Output(),
    5: NotZero(),
    6: Zero(),
    7: LessThan(),
    8: Equal(),
    9: AdjustRelativeBase(),
    99: Exit(),
}

class Runtime:
    def __init__(self, program, inputs=None):
        self.program = program
        self.i = 0
        self.inputs = inputs or []
        self.output_runtimes = []
        self.input_runtimes = []
        self.outputs = []
        self.relative_base = 0
        self.flags = Flags()

    def save(self):
        return self.program[:], self.relative_base, self.i

    def load(self, state):
        self.program = state[0]
        self.relative_base = state[1]
        self.i = state[2]

    def add_output_runtime(self, output_runtime):
        self.output_runtimes.append(output_runtime)

    def add_input_runtime(self, input_runtime):
        self.input_runtimes.append(input_runtime)

    def run_input_runtimes(self):
        for input_runtime in self.input_runtimes:
            input_runtime.run()

    def parse_opcode(self, opcode):
        self.flags.is_positional[PARAM_0] = opcode[2] == "0"
        self.flags.is_positional[PARAM_1] = opcode[1] == "0"
        self.flags.is_positional[PARAM_2] = opcode[0] == "0"
        self.flags.is_relative[PARAM_0] = opcode[2] == "2"
        self.flags.is_relative[PARAM_1] = opcode[1] == "2"
        self.flags.is_relative[PARAM_2] = opcode[0] == "2"
        return Opcodes[int(opcode[3:5])]

    def parse_param(self, param):
        i = self.i + param
        if self.flags.is_positional[param]:
            i = self.program[i]
        elif self.flags.is_relative[param]:
            i = self.program[i] + self.relative_base
        self.ensure_bounds(i)
        return self.program[i]

    def write_param(self, param, value):
        i = self.i + param
        if self.flags.is_relative[param]:
            i = self.program[i] + self.relative_base
        else:
            i = self.program[i]
        self.ensure_bounds(i)
        self.program[i] = value

    def ensure_bounds(self, i):
        if i >= len(self.program):
            self.program.extend([0] * (i - len(self.program) + 1))

    def output(self, output):
        for output_runtime in self.output_runtimes:
            output_runtime.inputs.append(output)
        self.outputs.append(output)

    def stop(self):
        self.i = len(self.program)

    def run(self):
        try:
            while self.i < len(self.program):
                opcode = str(self.program[self.i]).rjust(5, "0")
                opcode = self.parse_opcode(opcode)
                opcode.process(self)
        except StopIteration:
            return False
        return True
