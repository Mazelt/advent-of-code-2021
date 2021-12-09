import os
import sys
import timeit


def transform_data(raw_data):
    data = []
    for l in raw_data.split('\n'):
        if l == '':
            break
        command = l.split()
        data.append((str(command[0]), int(command[1])))
    return data

def travel(commands):
    horiz = 0
    depth = 0
    for c in commands:
        if c[0] == 'forward':
            horiz += c[1]
        if c[0] == 'down':
            depth += c[1]
        if c[0] == 'up':
            depth -= c[1]
    return horiz, depth

def test_travel():
    commands = [('forward', 5), ('down', 5), ('forward', 8), ('up', 3), ('down', 8), ('forward', 2)]
    h, d = travel(commands)
    assert(h == 15 and d == 10)

def travel_aim(commands):
    horiz = 0
    depth = 0
    aim = 0
    for c in commands:
        if c[0] == 'forward':
            horiz += c[1]
            depth += c[1]*aim
        if c[0] == 'down':
            aim += c[1]
        if c[0] == 'up':
            aim -= c[1]
    return horiz, depth

def test_travel_aim():
    commands = [('forward', 5), ('down', 5), ('forward', 8), ('up', 3), ('down', 8), ('forward', 2)]
    h, d = travel_aim(commands)
    assert(h == 15 and d == 60)


def ex2_a(data):
    horiz, depth = travel(data)
    print(f'Horizontal position is {horiz} with  depth {depth} and multiplication {horiz*depth}')

def ex2_b(data):
    horiz, depth = travel_aim(data)
    print(f'Horizontal position is {horiz} with  depth {depth} and multiplication {horiz*depth}')

def import_input(path):
    if not os.path.exists(path):
        print(f'input file not found {path}')
        exit(1)
    with open(path, 'r') as file:
        data = file.read()
    return data

if __name__ == '__main__':
    in_file = sys.argv[1]
    raw_data = import_input(in_file)
    data = transform_data(raw_data)
    test_travel()
    ex2_a(data)

    test_travel_aim()
    ex2_b(data)

    # timeit
    t_travel = timeit.timeit('travel(data)', number=1000, setup="from __main__ import travel, data")
    t_travel_aim = timeit.timeit('travel_aim(data)', number=1000, setup="from __main__ import travel_aim, data")
    print(f't_travel: {t_travel:.4f}')
    print(f't_travel_aim: {t_travel_aim:.4f}')