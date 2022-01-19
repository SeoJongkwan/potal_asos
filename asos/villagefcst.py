import pandas as pd
import numpy as np
import requests
import json
import psycopg2
from datetime import datetime, timedelta
from psycopg2.extensions import register_adapter, AsIs
psycopg2.extensions.register_adapter(np.int64, psycopg2._psycopg.AsIs)
from urllib.parse import urlencode, unquote

c_url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"
c_cert_key = "oEXb0KBtqI8V3TJAj1lmb9ZgDq8pwKDDnk2dAlaRpRltMNYuoTCT%2B1hlmImqXNWjK2qquaN9S7v2irGCoRccxw%3D%3D"

date = datetime.now() - timedelta(1)
date1 = date.strftime("%Y%m%d")
nx = 55
ny = 68
params = "?" + urlencode({
    'serviceKey': c_cert_key,
    'pageNo': 1,
    'numOfRows': 1000,
    'dataType': 'JSON',
    'base_date': date1,
    'base_time': 1700,
    'nx': nx,
    'ny': ny
})

res = requests.get(c_url+unquote(params)).json()
item = res['response']['body']['items']['item']
df = pd.DataFrame(item)

df['date'] = df['fcstDate']+df['fcstTime']
df['date'] = pd.to_datetime(df['date'], format='%Y%m%d%H%M')

temp = []
def extract_temp():
    for x in range(len(df)):
        if df['category'][x] == 'TMP':
            temp.append(x)
    df1 = df.iloc[temp]
    df2 = df1[['date','fcstValue']].reset_index(drop=True)
    return df2

village = extract_temp()
village.to_csv('/Users/bellk/PycharmProjects/potal_asos/asos/data/village_{}_{}_{}.csv'.format(date1, nx, ny), index=False)
print("date: {} - nx:{} / ny:{}".format(date1, nx, ny))
