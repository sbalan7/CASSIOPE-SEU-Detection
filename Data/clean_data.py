from datetime import datetime
import datetime as dt
import pandas as pd
import numpy as np
import time
import os

def clean_cassiope():
    data = pd.read_csv(os.path.join('Data','cassiope.txt'))
    data.columns = data.loc[0]
    data = data[1:]
    seu = data[0:22]
    nor = data[36:]

    seu = seu.assign(seu=1)
    nor = nor.assign(seu=0)

    data = pd.concat([seu, nor])

    data[['Date', 'Time']] = data['#Time'].str.split(' ', n=1, expand=True)
    data = data.reset_index(drop=True)
    data = data.drop(['#Time'], axis=1)
    data.loc[:,'Date'] = pd.to_datetime(data['Date'], format='%d/%m/%Y', errors='coerce')
    
    return data

def clean_omniweb():
    with open(os.path.join('Data', 'omni_headers.txt'), 'r') as f:
        lines = f.readlines()
