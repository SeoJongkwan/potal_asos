import pandas as pd
import numpy as np
import requests
import json
import psycopg2
import time
from apscheduler.schedulers.background import BackgroundScheduler
from psycopg2.extensions import register_adapter, AsIs
psycopg2.extensions.register_adapter(np.int64, psycopg2._psycopg.AsIs)

import warnings

warnings.simplefilter("ignore")
pd.set_option('mode.chained_assignment', None)

host='34.64.92.171'
dbname='solar_plant'
user='solar_plant'
password='ionsolarplantdev'
port='5432'

table = "solar_weather"
rtu_id = '0004_0001_W_0001'
date = '2022-01-17'

con = psycopg2.connect(host=host, dbname=dbname, user=user, password=password, port=port)
cursor = con.cursor()

def collect(rtu):
    env_cond = "rtu_id = '{}' and ud > '{}'".format(rtu_id, date)
    env_db = "SELECT * FROM {} WHERE {} ORDER BY ud DESC".format(table, env_cond)
    cursor.execute(env_db)
    env = pd.DataFrame(cursor.fetchall())
    env.columns = [desc[0] for desc in cursor.description]

    env = env[['ud', 's_ir', 'h_ir', 'm_t', 'a_t']]
    env['ud'] = pd.to_datetime(env['ud'], format='%Y-%m-%d %H:%M:%S')
    env['ud'] = env['ud'].apply(lambda t: t.replace(second=0, microsecond=0))
    print('rtu_id: {}'.format(rtu))
    # print('date: {}'.format(inv['ud'][0]))
    return env

env = collect(rtu_id)
# env = env1.set_index('ud').resample('1H').sum().reset_index()
# env['ud'] = pd.to_datetime(env['ud'], format='%Y-%m-%d %H:%M:%S')
# env = env['ud'].resample('1H').sum()
date = env['ud'][0].strftime("%Y%m%d")

env.to_csv("data/env_{}.csv".format(date), index=False)

