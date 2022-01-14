import pandas as pd
import numpy as np
import requests
import json
import psycopg2
from datetime import datetime, timedelta
from psycopg2.extensions import register_adapter, AsIs
psycopg2.extensions.register_adapter(np.int64, psycopg2._psycopg.AsIs)
from urllib.parse import urlencode, unquote

c_url = "http://apis.data.go.kr/1360000/AsosHourlyInfoService/getWthrDataList"
c_cert_key = "oEXb0KBtqI8V3TJAj1lmb9ZgDq8pwKDDnk2dAlaRpRltMNYuoTCT%2B1hlmImqXNWjK2qquaN9S7v2irGCoRccxw%3D%3D"

start1 = datetime.now() - timedelta(3)
start = start1.strftime("%Y%m%d")
end1 = datetime.now() - timedelta(1)
end = end1.strftime("%Y%m%d")
stnIds = 108

params = "?" + urlencode({
    'serviceKey': c_cert_key,
    'pageNo': 1,
    'numOfRows': 999,
    'dataType': 'JSON',
    'dataCd': 'ASOS',
    'dateCd': 'HR',
    'startDt': start,
    'startHh': '00',
    'endDt': end,
    'endHh': '23',
    'stnIds': stnIds,
})

res = requests.get(c_url+unquote(params)).json()
item = res['response']['body']['items']['item']
df = pd.DataFrame(item)
df['tm'] = pd.to_datetime(df['tm'], format='%Y-%m-%d %H:%M')
asos = df[['tm', 'ta']]

asos.to_csv('/Users/bellk/PycharmProjects/potal_asos/asos/asos_{}_{}.csv'.format(start, stnIds), index=False)
print('stnIds: {} / date: {} - {}'.format(stnIds, start, end))
