from advent import *

with open('input.txt') as input_file:
    lines = input_file.readlines()

asteroids = {}
y = 0
for line in lines:
    x = 0
    for c in line:
        if c == '#':
            asteroids[(x, y)] = True
        x += 1
    y += 1


def check_asteroids(asteroids, position):
    seen = defaultdict(list)
    for other_position in asteroids.keys():
        if position == other_position:
            continue
        d_x, d_y = tuple_subtract(other_position, position)
        angle = math.atan2(d_x, d_y)
        info = other_position, (d_x ** 2 + d_y ** 2)
        seen[angle].append(info)
    return seen


asteroid_los_counts = []
for position, asteroid in asteroids.items():
    count_same_angle = len(check_asteroids(asteroids, position))
    asteroid_los_counts.append((position, count_same_angle))

position, count = max(asteroid_los_counts, key=lambda x: x[1])
print(count)

asteroids_destroyed = 0
while True:
    asteroid_info = check_asteroids(asteroids, position)
    for angle in asteroid_info:
        asteroid_info[angle] = sorted(asteroid_info[angle], key=lambda x: x[1])

    angles = []
    for asteroids_at_angle in asteroid_info.values():
        asteroid = asteroids_at_angle[0][0]
        d_x, d_y = tuple_subtract(asteroid, position)
        angles.append((math.atan2(d_x, d_y), asteroid))

    clockwise_asteroids = map(lambda v: v[1], sorted(angles)[::-1])

    for asteroid in clockwise_asteroids:
        asteroids_destroyed += 1
        if asteroids_destroyed == 200:
            print(asteroid[0] * 100 + asteroid[1])
            break
        del asteroids[(asteroid[0], asteroid[1])]
