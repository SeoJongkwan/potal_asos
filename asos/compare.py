import pandas as pd
import numpy as np
import requests
import json
import sys
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns

import warnings
warnings.simplefilter("ignore")
pd.set_option('mode.chained_assignment', None)


meteobllue = pd.read_csv('meteoblue_20220114_37.49_127.03.csv')
village = pd.read_csv('village_20220113_61_125.csv')
asos = pd.read_csv('asos_20220111_108.csv')

meteobllue['time'] = pd.to_datetime(meteobllue['time'], format='%Y-%m-%d %H:%M')
village['date'] = pd.to_datetime(village['date'], format='%Y-%m-%d %H:%M')
asos['tm'] = pd.to_datetime(asos['tm'], format='%Y-%m-%d %H:%M')

df = pd.merge(meteobllue.set_index('time'), village.set_index('date'), left_index=True, right_index=True).reset_index()
df1 = pd.merge(df.set_index('index'), asos.set_index('tm'), left_index=True, right_index=True).reset_index()

# df5 = df4.drop_duplicates(['index'], keep='first').reset_index(drop=True)
weather = df[['index', 'temperature', 'fcstValue']]
weather.columns = ['date', 'meteoblue', 'asos']
weather['date'] = pd.to_datetime(weather['date'], format='%Y-%m-%d %H:%M')
weather['asos'] = weather['asos'].astype('float')

# start = weather['date'].dt.strftime('%Y-%m-%d')[0]
# weather.to_csv('weather{}_{}_{}.csv'.format(start))

fig, ax1 = plt.subplots(figsize=(14, 6))
xtick = list(np.unique(weather['date'].dt.strftime('%m-%d %H')))
sns.lineplot(x=xtick, y=weather['meteoblue'], color='b', label='meteoblue', ax=ax1)
# ax2 = ax1.twinx()
sns.lineplot(x=xtick, y=weather['asos'], color='r', label='asos', ax=ax1)
ax1.set_xticklabels(xtick, rotation=90)
ax1.legend(loc=0)
ax1.grid(True, axis='y', linestyle='dashed')
ax1.set(xlabel='date', ylabel='temp', title='Temp Compare: Meteoblue and Asos')
plt.tight_layout()
plt.show()
