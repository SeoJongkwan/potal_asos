import pandas as pd
import numpy as np
import requests
import json
import sys
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
from urllib.parse import urlencode, unquote

import warnings
warnings.simplefilter("ignore")
pd.set_option('mode.chained_assignment', None)

c_url = "http://my.meteoblue.com/packages/solar-1h"
c_cert_key = "kb0cpzJfvDZLMrTX"

#latitude: 37.49, longitude: 127.03,
lat = '34.876'
lon = '126.681'
# lat = sys.argv[1]
# lon = sys.argv[2]

params = "?" + urlencode({
    'lon': lon,
    'lat': lat,
    'apikey': c_cert_key,
})

url = c_url+unquote(params)
# print(url)
res = requests.get(url).json()
key = res.keys()

print("meta: " , res['metadata'])
# df = pd.DataFrame("res['metadata'])
df1 = pd.DataFrame(res['data_1h'])
df1['time'] = pd.to_datetime(df1['time'], format='%Y-%m-%d %H:%M')
# df1['time'] = df1['time'].dt.strftime('%Y-%m-%d %H:%M')

weather = df1[['time', 'extraterrestrialradiation_instant']]
start = weather['time'].dt.strftime('%Y%m%d')[0]
weather.to_csv('/Users/bellk/PycharmProjects/potal_asos/asos/meteoblue_irr_{}_{}_{}.csv'.format(start, lat, lon), index=False)
print("date: {} - lon:{} / lat:{}".format(start, lon, lat))


# df3 = villagefcst.extract_temp()
# df3['date'] = df3['date'].dt.strftime('%Y-%m-%d %H:%M')
#
#
# df4 = pd.merge(df1.set_index('time'), df3.set_index('date'), left_index=True, right_index=True).reset_index()
# df5 = df4.drop_duplicates(['index'], keep='first').reset_index(drop=True)
# weather = df5[['index', 'temperature', 'fcstValue']]
# weather.columns = ['date', 'meteoblue', 'asos']
# weather['date'] = pd.to_datetime(weather['date'], format='%Y-%m-%d %H:%M')
# weather['asos'] = weather['asos'].astype('float')
#
# start = weather['date'].dt.strftime('%Y-%m-%d')[0]
# weather.to_csv('weather{}_{}_{}.csv'.format(lat, lon, start))
#
# fig, ax1 = plt.subplots(figsize=(14, 6))
# xtick = list(np.unique(weather['date'].dt.strftime('%m-%d %H')))
# sns.lineplot(x=xtick, y=weather['meteoblue'], color='b', label='meteoblue', ax=ax1)
# # ax2 = ax1.twinx()
# sns.lineplot(x=xtick, y=weather['asos'], color='r', label='asos', ax=ax1)
# ax1.set_xticklabels(xtick, rotation=90)
# ax1.legend(loc=0)
# ax1.grid(True, axis='y', linestyle='dashed')
# ax1.set(xlabel='date', ylabel='temp', title='Temp Compare: Meteoblue and Asos - {} / {}'.format(lat, lon))
# plt.tight_layout()
# plt.show()
