import os
import sys
import timeit

def transform_data(data):
    return [int(x) for x in data.split()]

def count_increase(data):
    count = 0
    for i in range(len(data)-1):
        if data[i+1] > data[i]:
            count += 1
    return count

def test_count_increase():
    t0 = [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]
    t1 = [0, 1, 2, 3] # 3
    t2 = [0, 4, 2, 1] # 1
    t3 = [1, 2, 1, 5] # 2
    assert(count_increase(t0) == 7)
    assert(count_increase(t1) == 3)
    assert(count_increase(t2) == 1)
    assert(count_increase(t3) == 2)

def count_increase_window(data, size):
    count = 0
    for i in range(len(data)-size):
        window_a = sum(data[i:i+size])
        window_b = sum(data[i+1:i+size+1])
        if window_b > window_a:
            count += 1
    return count


def count_increase_window_perf(data, size):
    count = 0
    window_a = sum(data[0:size])
    window_b = window_a - data[0] + data[size]
    if window_b > window_a:
        count += 1
    for i in range(1, len(data)-size):
        window_a = window_b
        window_b = window_a - data[i] + data[i+size]
        if window_b > window_a:
            count += 1
    return count

def test_count_increase_window():
    t0 = [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]
    t1 = [0, 1, 2, 3] # 1,3,5 -> 2
    t2 = [0, 4, 2, 1] # 4, 6, 3 -> 1
    t3 = [1, 2, 1, 5] # 3, 3, 6 -> 1
    t4 = [2, 1, 1, 3, 5, 2, 3] # 4, 5, 9, 10, 10 -> 3 
    assert(count_increase_window(t0,3) == 5)
    assert(count_increase_window(t1,2) == 2)
    assert(count_increase_window(t2,2) == 1)
    assert(count_increase_window(t3,2) == 1)
    assert(count_increase_window(t4,3) == 3)
    assert(count_increase_window_perf(t0,3) == 5)
    assert(count_increase_window_perf(t1,2) == 2)
    assert(count_increase_window_perf(t2,2) == 1)
    assert(count_increase_window_perf(t3,2) == 1)
    assert(count_increase_window_perf(t4,3) == 3)


def ex1_a(data):
    increases = count_increase(data)
    print(f'Found {increases} increases')

def ex1_b(data):
    increases = count_increase_window(data, 3)
    print(f'Found {increases} window increases')

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
    test_count_increase()
    ex1_a(data)
    test_count_increase_window()
    ex1_b(data)

    # timeit
    t_count_increase = timeit.timeit('count_increase(data)', number=1000, setup="from __main__ import count_increase, data")
    t_count_increase_window_1 = timeit.timeit('count_increase_window(data,1)', number=1000, setup="from __main__ import count_increase_window, data")
    t_count_increase_window_2 = timeit.timeit('count_increase_window(data,2)', number=1000, setup="from __main__ import count_increase_window, data")
    t_count_increase_window_3 = timeit.timeit('count_increase_window(data,3)', number=1000, setup="from __main__ import count_increase_window, data")
    t_count_increase_window_perf_1 = timeit.timeit('count_increase_window_perf(data,1)', number=1000, setup="from __main__ import count_increase_window_perf, data")
    t_count_increase_window_perf_2 = timeit.timeit('count_increase_window_perf(data,2)', number=1000, setup="from __main__ import count_increase_window_perf, data")
    t_count_increase_window_perf_3 = timeit.timeit('count_increase_window_perf(data,3)', number=1000, setup="from __main__ import count_increase_window_perf, data")
    print(f't_count_increase: {t_count_increase:.4f}')
    print(f't_count_increase_window 1: {t_count_increase_window_1:.4f}')
    print(f't_count_increase_window 2: {t_count_increase_window_2:.4f}')
    print(f't_count_increase_window 3: {t_count_increase_window_3:.4f}')
    print(f't_count_increase_window_perf 1: {t_count_increase_window_perf_1:.4f}')
    print(f't_count_increase_window_perf 2: {t_count_increase_window_perf_2:.4f}')
    print(f't_count_increase_window_perf 3: {t_count_increase_window_perf_3:.4f}')