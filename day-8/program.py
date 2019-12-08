from collections import Counter

with open('input.txt') as input_file:
    lines = input_file.readlines()

width = 25
height = 6

line = lines[0]
rows = [line[i:i+25] for i in range(0, len(line), 25)]
layers = [rows[i:i+6] for i in range(0, len(rows), 6)]

ans = 0
min = 1e999
for layer in layers:
    counter = Counter([pixel for line in layer for pixel in line])
    count = counter['0']
    if count < min:
        min = count
        ans = counter['1'] * counter['2']

print(ans)

for y in range(height):
    line = ''
    for x in range(width):
        pixel = '2'
        for layer in layers:
            color_pixel = layer[y][x]
            if color_pixel != '2':
                pixel = color_pixel
                break
        if pixel == '1':
            line += '#'
        else:
            line += ' '
    print(line)
