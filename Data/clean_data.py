from datetime import datetime
import datetime as dt
import pandas as pd
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
    data = data.drop(['#Time', 'Time'], axis=1)
    data.loc[:,'Date'] = pd.to_datetime(data['Date'], format='%d/%m/%Y', errors='coerce')
    
    return data

def clean_omniweb():
    with open(os.path.join('Data', 'omni_headers.txt'), 'r') as f:
        lines = f.readlines()

    data = pd.read_fwf(os.path.join('Data', 'omni_data.txt'), header=None)
    data.columns = [line[3:30].rstrip() for line in lines[4:]]
    
    yyyyddd = [str(data.YEAR[i]) + str(data.DOY[i]) for i in range(len(data))]
    data['Date'] = [datetime.strftime(datetime.strptime(yyyyddd[i], '%Y%j'), '%Y/%m/%d') for i in range(len(data))]
    data['Date'] = pd.to_datetime(data['Date'], format='%Y/%m/%d', errors='coerce')
    
    data = data.drop(['YEAR', 'DOY', 'Hour'], axis=1)

    return data

print('Reading data...')
tic = time.time()
cas = clean_cassiope()
omn = clean_omniweb()
toc = time.time()
print('Done in {:.3f} seconds'.format(toc-tic))

df = cas.merge(omn, how='inner', on='Date')
df['Date'] = (df['Date'] - dt.datetime(1970,1,1)).dt.total_seconds()
print(df.columns)
path = 'cleaned_data.csv'
df.to_csv(path, index=False)
print('File saved at {}'.format(path))
