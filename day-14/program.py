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


class ReagentInfo:
    def __init__(self, name, number):
        self.name = name
        self.number = number


in_formulas = defaultdict(list)
out_formulas = {}

ore = 'ORE'
fuel = 'FUEL'
for line in lines:
    inputs, output = line.split("=>")
    output_number, output_name = output.strip().split(" ")

    formula = Formula()
    formula.output = ReagentInfo(output_name, int(output_number))
    for input_reagent in inputs.split(","):
        input_reagent = input_reagent.strip()
        input_number, input_name = input_reagent.split(" ")
        formula.inputs.append(ReagentInfo(input_name, int(input_number)))
        in_formulas[input_name].append(formula)
    out_formulas[output_name] = formula

needed = defaultdict(int)
producing = defaultdict(int)


def produce(name):
    formula = out_formulas[name]
    out_reagent = formula.output
    count = math.ceil(
        max(0, needed[out_reagent.name] - producing[out_reagent.name])
        / out_reagent.number)
    producing[out_reagent.name] += count * out_reagent.number
    for in_reagent in formula.inputs:
        needed[in_reagent.name] += count * in_reagent.number

    for in_reagent in formula.inputs:
        if in_reagent.name != ore:
            produce(in_reagent.name)


needed[fuel] = 1
produce(fuel)
print(needed[ore])

ore_reserve = 1000000000000
fuel_to_produce = 0
fuel_jump = 1
narrowing = False

while True:
    needed.clear()
    producing.clear()
    needed[fuel] = fuel_to_produce
    produce(fuel)
    if needed[ore] > ore_reserve:
        narrowing = True
        fuel_jump = max(1, fuel_jump // 2)
        fuel_to_produce -= fuel_jump
    elif not narrowing:
        fuel_jump *= 2
        fuel_to_produce += fuel_jump
    else:
        if fuel_jump == 1:
            break
        fuel_to_produce += fuel_jump

print(fuel_to_produce)
