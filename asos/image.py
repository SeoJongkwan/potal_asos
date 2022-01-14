import pandas as pd
import numpy as np
import requests
import json
import psycopg2
from PIL import Image
from datetime import datetime, timedelta
from psycopg2.extensions import register_adapter, AsIs
psycopg2.extensions.register_adapter(np.int64, psycopg2._psycopg.AsIs)
from urllib.parse import urlencode, unquote


#천리안 위성2A
c_url = "http://apis.data.go.kr/1360000/SatlitImgInfoService/getInsightSatlit"
c_cert_key = "oEXb0KBtqI8V3TJAj1lmb9ZgDq8pwKDDnk2dAlaRpRltMNYuoTCT%2B1hlmImqXNWjK2qquaN9S7v2irGCoRccxw%3D%3D"

params = "?" + urlencode({
    'serviceKey': c_cert_key,
    'pageNo': '1',
    'numOfRows': '1000',
    'dataType': 'JSON',
    'sat': 'G2',
    'data': 'vi006',
    'area': 'ko',
    'time': datetime.now().strftime("%Y%m%d")
})


res = requests.get(c_url+unquote(params))
data = res.content.decode('utf-8')
data_json = json.loads(data)

img_item = data_json['response']['body']['items']['item']
img = img_item[0]
img['satImgC-file'][0]

for k in img.values():
    print(k[0])