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

mb1 = pd.read_csv('data/meteoblue_irr_20220117_34.876_126.681.csv')
mb2 = pd.read_csv('data/meteoblue_irr_20220118_34.876_126.681.csv')
# mb3 = pd.read_csv('data/meteoblue_20220117_34.876_126.681.csv')
mb4 = pd.read_csv('data/meteoblue_20220118_34.876_126.681.csv')

mb1['time'] = pd.to_datetime(mb1['time'], format='%Y-%m-%d %H:%M')
mb2['time'] = pd.to_datetime(mb2['time'], format='%Y-%m-%d %H:%M')
# mb3['time'] = pd.to_datetime(mb3['time'], format='%Y-%m-%d %H:%M')
mb4['time'] = pd.to_datetime(mb4['time'], format='%Y-%m-%d %H:%M')

mb_irr_merge = pd.concat([mb1.set_index('time'), mb2.set_index('time')], axis=1)
# mb_tp_merge = pd.concat([mb3.set_index('time'), mb4.set_index('time')], axis=1)

def missing_fill(df):
    for i in range(len(df)):
        if np.isnan(df.iloc[i,0]) == True:
            df.iloc[i,0] = df.iloc[i,1]
        elif np.isnan(df.iloc[i,1]) == True:
            df.iloc[i, 1] = df.iloc[i, 0]
        else:
            pass
    return df

mb_irr1 = missing_fill(mb_irr_merge).reset_index()
mb_irr1.columns = ['time', 'irr', 'irr1']
mb_irr = mb_irr1.drop(mb_irr1.columns[2], axis=1)

mb_tp = mb4.copy()
mb = pd.merge(mb_irr.set_index('time'), mb_tp.set_index('time'), left_index=True, right_index=True).reset_index()

env = pd.read_csv('data/env_20220118.csv')
env['ud'] = pd.to_datetime(env['ud'], format='%Y-%m-%d %H:%M')
env = env[['ud', 'a_t', 's_ir']]
mb_real = pd.merge(mb.set_index('time'), env.set_index('ud'), left_index=True, right_index=True).reset_index().rename(columns={"index":"time"})
mb_real = mb_real[['time','a_t','temperature','s_ir','irr']]


# v1 = pd.read_csv('village_20220115_61_125.csv')
#
# as1 = pd.read_csv('data/asos_20220113_108.csv')
# as1['tm'] = pd.to_datetime(as1['tm'], format='%Y-%m-%d %H:%M')

# as2 = pd.read_csv('asos_20220111_108.csv')



# meteobllue['time'] = pd.to_datetime(meteobllue['time'], format='%Y-%m-%d %H:%M')
# village['date'] = pd.to_datetime(village['date'], format='%Y-%m-%d %H:%M')
# asos['tm'] = pd.to_datetime(asos['tm'], format='%Y-%m-%d %H:%M')

# df = pd.merge(meteobllue.set_index('time'), village.set_index('date'), left_index=True, right_index=True).reset_index()
# df1 = pd.merge(df.set_index('index'), asos.set_index('tm'), left_index=True, right_index=True).reset_index()
#
# # df5 = df4.drop_duplicates(['index'], keep='first').reset_index(drop=True)
# weather = df[['index', 'temperature', 'fcstValue']]
# weather.columns = ['date', 'meteoblue', 'asos']
# weather['date'] = pd.to_datetime(weather['date'], format='%Y-%m-%d %H:%M')
# weather['asos'] = weather['asos'].astype('float')
#
# # start = weather['date'].dt.strftime('%Y-%m-%d')[0]
# # weather.to_csv('weather{}_{}_{}.csv'.format(start))


def plot(df):
    plt.style.use('dark_background')
    fig, ax1 = plt.subplots(figsize=(20, 6))
    xtick = list(np.unique(df['time'].dt.strftime('%m-%d %H')))
    sns.lineplot(x=xtick, y=df['a_t'], color='salmon', label='top_temp', ax=ax1)
    sns.lineplot(x=xtick, y=df['temperature'], color='r', label='mb_temp', ax=ax1)
    ax2 = ax1.twinx()
    sns.lineplot(x=xtick, y=df['s_ir'], color='y', label='top_irr', ax=ax2)
    sns.lineplot(x=xtick, y=df['irr'], color='g', label='mb_irr', ax=ax2)

    ax1.set_xticklabels(xtick, rotation=90)
    ax1.legend(loc=0)
    ax2.legend(loc=2)
    # ax1.grid(True, axis='y', linestyle='dashed')
    ax1.set(xlabel='date', title='TopInfra vs Meteoblue')
    plt.tight_layout()
    plt.show()

plot(mb_real)