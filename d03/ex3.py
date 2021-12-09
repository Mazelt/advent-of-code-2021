import os
import sys
import timeit
from math import ceil


def gamma(data):
    mask = [0]*len(data[0])
    for b in data:
        for i in range(len(b)):
            mask[i] += int(b[i])
    half = ceil(len(data)/2)
    gamma = [0]*len(data[0])
    for i, e in enumerate(mask):
        if e >= half:
            gamma[i] = 1
        else:
            gamma[i] = 0
    return gamma

def gamma_special(data, start, end, index={}):
    b_len = len(data[0])
    mask = [0]*b_len
    if index:
        for j in index:
            for i in range(start, min(b_len,end)):
                mask[i] += int(data[j][i])
        half = ceil(len(index)/2)
    else:
        for b in data:
            for i in range(start, min(len(b),end)):
                mask[i] += int(b[i])
        half = ceil(len(data)/2)
    gamma = [0]*b_len
    for i, e in enumerate(mask):
        if e >= half:
            gamma[i] = 1
        else:
            gamma[i] = 0
    return gamma[start:end]
    
def gamma_special_old(data):
    mask = [0]*len(data[0])
    for b in data:
        for i in range(len(b)):
            if int(b[i]):
                mask[i] += 1
            else:
                mask[i] -= 1
    gamma = [0]*len(data[0])
    for i, e in enumerate(mask):
        if e >= 0:
            gamma[i] = 1
        else:
            gamma[i] = 0
    return gamma

def test_gamma():
    report = ['00100','11110','10110','10111','10101','01111','00111','11100','10000','11001','00010','01010']
    report_eq = ['00100','11110','10110','00111']
    test_index = {1,2,4,5,8}
    g = gamma(report)
    g_s = gamma_special(report, 0, len(report[0]))
    g_s_eq = gamma_special(report_eq, 0, len(report[0]))
    g_s_2 = gamma_special(report, 1, len(report[0]))
    g_s_3 = gamma_special(report, 1, 4)
    g_s_i = gamma_special(report, 0, len(report[0]), index=test_index)
    report_i = [report[i] for i in test_index]
    g_i = gamma(report_i)
    g_s_o = gamma_special_old(report)
    assert(g == [1,0,1,1,0])
    assert(g_s == [1,0,1,1,0])
    assert(g_s_o == g)
    assert(g_s_2 == [0,1,1,0])
    assert(g_s_3 == [0,1,1])
    assert(g_s_i == g_i)
    assert(g_s_eq[0] == 1)


def epsilon(gamma):
    epsilon = []
    for e in gamma:
        if e == 0:
            epsilon.append(1)
        else:
            epsilon.append(0)
    return epsilon

def test_epsilon():
    g = [1,0,1,1,0]
    eps = epsilon(g)
    assert(eps == [0,1,0,0,1])


def oxygen(data):
    index = set([])
    # for c in len(data[0]):
    g1 = gamma_special(data, 0, 1)
    for i in range(len(data)):
        if data[i][0] == str(g1[0]):
            index.add(i)
    c = 1
    while(len(index)> 1):
        g = gamma_special(data, c, c+1, index=index)
        for i in index.copy():
            if data[i][c] != str(g[0]):
                index.remove(i)
        c += 1        
    return data[list(index)[0]]

def oxygen_co2(data):
    index_ox = set([])
    index_co2 = set([])
    # for c in len(data[0]):
    g1 = gamma_special(data, 0, 1)
    for i in range(len(data)):
        if data[i][0] == str(g1[0]):
            index_ox.add(i)
        else:
            index_co2.add(i)
    c = 1
    while(len(index_ox)> 1 or len(index_co2) > 1):
        if len(index_ox) > 1:
            g_ox = gamma_special(data, c, c+1, index=index_ox)
            for i in index_ox.copy():
                if data[i][c] != str(g_ox[0]):
                    index_ox.remove(i)
        if len(index_co2) > 1:
            g_co2 = gamma_special(data, c, c+1, index=index_co2)
            for i in index_co2.copy():
                if data[i][c] == str(g_co2[0]):
                    index_co2.remove(i)
                
        c += 1        
    return data[list(index_ox)[0]], data[list(index_co2)[0]]

def test_oxygen():
    report = ['00100','11110','10110','10111','10101','01111','00111','11100','10000','11001','00010','01010']
    # ['d','d','0110','0111','0101','d','d','d','0000','d','d','d']
    ox = oxygen(report)
    assert(ox == '10111')
    ox_2, co2 = oxygen_co2(report)
    assert(ox == ox_2)
    assert(co2 == '01010')

def ex3_a(data):
    g = gamma(data)
    eps = epsilon(g)
    g_dez = int(''.join(str(x) for x in g),2)
    eps_dez = int(''.join(str(x) for x in eps),2)
    print(f'Gamma rate is {g} = {g_dez} , epsilon rate is {eps} = {eps_dez} and power is {g_dez*eps_dez}')

def ex3_b(data):
    ox, co2 = oxygen_co2(data)
    ox_dez = int(''.join(str(x) for x in ox),2)
    co2_dez = int(''.join(str(x) for x in co2),2)
    print(f'Oxygen rate is {ox} = {ox_dez} , epsilon rate is {co2} = {co2_dez} and life support rating is {ox_dez*co2_dez}')



def transform_data(raw_data):
    return raw_data.split()

def import_input(path):
    if not os.path.exists(path):
        print(f'input file not found {path}')
        exit(1)
    with open(path, 'r') as file:
        data = file.read()
    return data

if __name__ == '__main__':
    in_file = './input.txt'
    # in_file = sys.argv[1]
    raw_data = import_input(in_file)
    data = transform_data(raw_data)
    # print(data[:4])
    test_gamma()
    test_epsilon()
    test_oxygen()
    ex3_a(data)
    ex3_b(data)

    
    # timeit
    t_gamma = timeit.timeit('gamma(data)', number=1000, setup="from __main__ import gamma, data")
    t_gamma_special = timeit.timeit('gamma_special(data,0,12)', number=1000, setup="from __main__ import gamma_special, data")
    t_oxygen = timeit.timeit('oxygen(data)', number=1000, setup="from __main__ import oxygen, data")
    t_oxygen_co2 = timeit.timeit('oxygen_co2(data)', number=1000, setup="from __main__ import oxygen_co2, data")
    print(f't_gamma: {t_gamma:.4f}')
    print(f't_gamma_special: {t_gamma_special:.4f}')
    print(f't_oxygen: {t_oxygen:.4f}')
    print(f't_oxygen_co2: {t_oxygen_co2:.4f}')