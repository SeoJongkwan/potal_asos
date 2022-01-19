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

c_url = "http://my.meteoblue.com/packages/basic-1h_basic-day"
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

weather = df1[['time', 'temperature']]
start = weather['time'].dt.strftime('%Y%m%d')[0]
weather.to_csv('/Users/bellk/PycharmProjects/potal_asos/asos/data/meteoblue_{}_{}_{}.csv'.format(start, lat, lon), index=False)
print("date: {} - lon:{} / lat:{}".format(start, lon, lat))

