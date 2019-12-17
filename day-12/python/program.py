from advent import *

with open('../input.txt') as input_file:
    lines = input_file.readlines()

moons = []
for line in lines:
    parts = line.split(',')
    pos = []
    for i in range(0, 3):
        pos.append(int(parts[i].replace('>', '').split('=')[1]))
    moons.append([pos, [0, 0, 0]])


def step_dimension(moons, dimension):
    for moon_a, moon_b in combinations(moons, 2):
        if moon_a[0][dimension] > moon_b[0][dimension]:
            moon_a[1][dimension] -= 1
            moon_b[1][dimension] += 1
        elif moon_a[0][dimension] < moon_b[0][dimension]:
            moon_a[1][dimension] += 1
            moon_b[1][dimension] -= 1

    for moon in moons:
        moon[0][dimension] += moon[1][dimension]


for t in range(1000):
    for dimension in range(3):
        step_dimension(moons, dimension)


def energy(moon):
    return sum(map(abs, moon[0])) * sum(map(abs, moon[1]))


print(sum(energy(moon) for moon in moons))

periods = {}
for dimension in range(3):
    seen = set()
    t = 0
    while True:
        key = str([moon[0] + moon[1] for moon in moons])
        if key in seen:
            periods[dimension] = t
            break

        seen.add(key)
        step_dimension(moons, dimension)
        t += 1

print(lcm(periods[0], lcm(periods[1], periods[2])))
