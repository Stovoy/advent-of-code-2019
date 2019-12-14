import math
from intcode import Runtime
from collections import defaultdict, Counter

with open('input.txt') as input_file:
    lines = input_file.readlines()

formulas = {}


class Formula:
    def __init__(self):
        self.inputs = []
        self.output = None

    def __repr__(self):
        return f'{self.inputs} -> {self.output}'


class ReagentInfo:
    def __init__(self, name, number):
        self.name = name
        self.number = number

    def __repr__(self):
        return f'{self.name}: {self.number}'


in_formulas = defaultdict(lambda: [])
out_formulas = {}

start = 'ORE'
end = 'FUEL'
for line in lines:
    l, r = line.split("=>")
    o_num, o_name = r.strip().split(" ")

    formula = Formula()
    formula.output = ReagentInfo(o_name, int(o_num))
    for in_chem in l.split(","):
        in_chem = in_chem.strip()
        i_num, i_name = in_chem.split(" ")
        formula.inputs.append(ReagentInfo(i_name, int(i_num)))
        in_formulas[i_name].append(formula)
    out_formulas[o_name] = formula


def produce(name, needed, producing):
    formula = out_formulas[name]
    out_reagent = formula.output
    count = math.ceil(
        max(0, needed[out_reagent.name] - producing[out_reagent.name])
        / out_reagent.number)
    producing[out_reagent.name] += count * out_reagent.number
    for in_reagent in formula.inputs:
        needed[in_reagent.name] += count * in_reagent.number

    for in_reagent in formula.inputs:
        if in_reagent.name != start:
            produce(in_reagent.name, needed, producing)


needed = defaultdict(lambda: 0)
producing = defaultdict(lambda: 0)
needed[end] = 1
produce(end, needed, producing)
print(needed[start])

search = 1000000000000
i = 0
jump = 1
narrowing = False

while True:
    needed = defaultdict(lambda: 0)
    producing = defaultdict(lambda: 0)
    needed[end] = i
    produce(end, needed, producing)
    if needed[start] > search:
        narrowing = True
        jump = max(1, jump // 2)
        i -= jump
    elif not narrowing:
        jump *= 2
        i += jump
    else:
        if jump == 1:
            break
        i += jump

print(i)
