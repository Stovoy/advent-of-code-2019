from collections import Counter

with open('input.txt') as input_file:
    lines = input_file.readlines()


def p1(s):
    return bool({2, 3, 4, 5, 6} & set(Counter(s).values())) and sorted(s) == list(s)


def p2(s):
    return 2 in Counter(s).values() and sorted(s) == list(s)


l, r = list(map(int, lines[0].split('-')))
print(sum(p1(str(n)) for n in range(l, r)))
print(sum(p2(str(n)) for n in range(l, r)))
