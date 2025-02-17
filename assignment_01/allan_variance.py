#!/usr/bin/env python3

import numpy                as np
import matplotlib.pyplot    as plt
import pandas               as pd
import allantools

def read_data(fname : str):
    df = pd.read_excel(fname, 'Sheet1', parse_datas=['Timet(s)', 'Deviation(Hz)'])
    #  print(df.head())
    var1 = df['Timet(s)'].tolist()
    var2 = df['Deviation(Hz)'].tolist()
    return var1, var2

def partial_average(fract_data: list,
                    step      : int) :
    nparts = (len(fract_data) - 1) // step
    out    = []
    for i in range(nparts) :
        partial_sum = .0
        for j in range(i, i+step + 1):
            partial_sum += fract_data[j]
        out.append(partial_sum / step )
    return out

def calc_deviation(pavgs : list) :
    sum_of_dy2 = .0
    for i in range(len(pavgs) - 1):
        sum_of_dy2 += (pavgs[i+1] - pavgs[i]) ** 2
    return np.sqrt(sum_of_dy2 / (2*len(pavgs) - 2))

def main() :
    #  f_0 = 1
    f_0 = 3e8 / 730e-9 # the frequency of 730nm light
    timet, fract_data = read_data(r'./Ca_clock_transition_data.xls')
    timet.pop()
    fract_data.pop()
    
    y = []
    x = timet[:len(fract_data)//2]

    for i in range(len(fract_data) // 2):
        pavgs = partial_average(fract_data, i + 1)
        devia = calc_deviation (pavgs)
        y.append(devia / f_0)

    plt.loglog(x, y)
    plt.xlabel('$\\tau / sec$')
    plt.ylabel('$\delta f / f$')
    plt.savefig('ad.png', dpi=400)
    #  plt.show()

def main_use_allantools() :
    f_0 = 3e8 / 730e-9 # the frequency of 730nm light
    timet, fract_data = read_data(r'./Ca_clock_transition_data.xls')
    timet.pop()
    fract_data.pop()

    for i, elem in enumerate(fract_data) :
        fract_data[i] = elem / f_0
    (t2, ad, ade, adn) = allantools.oadev(fract_data, rate=11.2,
            data_type="freq", taus = [i for i in range(1, len(timet) + 1)])
    plt.loglog(t2, ad)
    plt.savefig('ad.png', dpi=400)
    #  plt.show()

def debug_partial_average(step: int) :
    vec = [i for i in range(1, 21)]
    pavg = partial_average(vec, step)
    print('step = {}, vec.size() = {}, pavg.size = {}'
            .format(step, len(vec), len(pavg)))
    print(vec)
    print(pavg, '\n')

def debug_deviation() :
    vec = [i for i in range(1, 21)]
    devia = calc_deviation(vec)
    print(vec)
    print(devia)

if __name__ == "__main__" :
    #  for i in range(1, 10):
        #  debug_partial_average(i)
    #  debug_deviation()
    main()
    #  main_use_allantools()
