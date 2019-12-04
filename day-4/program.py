with open('input.txt') as input_file:
    lines = input_file.readlines()


def p1(s):
    pairs = list(zip(s, s[1:]))
    return any(a == b for a, b in pairs) and all(b >= a for a, b in pairs)


def p2(s):
    pairs = list(zip(s, s[1:]))
    match = [False] + [a == b for a, b in pairs] + [False]
    return any(not a and b and not c for a, b, c in zip(match, match[1:], match[2:])) and all(
        b >= a for a, b in pairs)


l, r = list(map(int, lines[0].split('-')))
print(sum(p1(str(n)) for n in range(l, r)))
print(sum(p2(str(n)) for n in range(l, r)))
