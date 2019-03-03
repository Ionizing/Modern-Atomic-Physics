#!/usr/bin/env python3

import numpy                as np
import matplotlib.pyplot    as plt
import pandas               as pd

def read_data(fname : str):
    df = pd.read_excel(fname, 'Sheet1', parse_datas=['Timet(s)', 'Deviation(Hz)'])
    #  print(df.head())
    var1 = df['Timet(s)'].tolist()
    var2 = df['Deviation(Hz)'].tolist()
    return var1, var2

def partial_average(fract_data: list,
                    step      : int) :
    nparts = len(fract_data) // step
    out    = []
    for i in range(nparts) :
        partial_sum = .0
        for j in range(i, i+step):
            partial_sum += fract_data[j]
        out.append(partial_sum / step)
    return out

def calc_deviation(pavgs : list) :
    sum_of_dy2 = .0
    for i in range(len(pavgs) - 1):
        sum_of_dy2 += (pavgs[i+1] - pavgs[i]) ** 2
    return np.sqrt(sum_of_dy2 / (2*len(pavgs) - 2))

def main() :
    f = 3e8 / 730e-9 # the frequency of 730nm light
    timet, fract_data = read_data(r'./Ca_clock_transition_data.xls')
    timet.pop()
    fract_data.pop()

    y = []
    x = timet[:len(fract_data)//2]

    for i in range(len(fract_data) // 2):
        pavgs = partial_average(fract_data, i + 1)
        devia = calc_deviation (pavgs)
        y.append(devia / f)

    plt.loglog(x, y)
    plt.show()

if __name__ == "__main__" :
    main()
