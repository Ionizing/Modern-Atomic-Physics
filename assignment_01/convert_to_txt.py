#!/usr/bin/env python3

import pandas as pd
import numpy as np

def read_xls(fname: str) :
    df = pd.read_excel(fname, 'Sheet1', parse_datas=['Deviation(Hz)', 'Timet(s)'])
    deviation = df['Deviation(Hz)'].tolist()
    deviation.pop()
    timet     = df['Timet(s)'].tolist()
    timet.pop()
    return np.array(timet), np.array(deviation)

def main() :
    timet, deviation = read_xls(r'./Ca_clock_transition_data.xls')
    np.savetxt('deviation.txt', deviation, delimiter='\n', header='{}'.format(deviation.size))

if __name__ == "__main__" :
    main()
