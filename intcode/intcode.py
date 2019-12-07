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
        self.flags = Flags()

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
        return Opcodes[int(opcode[3:5])]

    def parse_param(self, param):
        i = self.i + param
        return self.program[self.program[i]] if self.flags.is_positional[param] else self.program[i]

    def write_param(self, param, value):
        self.program[self.program[self.i + param]] = value

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
            pass
