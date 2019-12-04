with open('input.txt') as input_file:
    lines = input_file.readlines()


total_fuel = 0
for line in lines:
    total_fuel += int(line) // 3 - 2

print(total_fuel)

total_fuel = 0
for line in lines:
    number = int(line) // 3 - 2
    total_fuel += number
    while number > 0:
        number = max(number // 3 - 2, 0)
        total_fuel += number

print(total_fuel)
