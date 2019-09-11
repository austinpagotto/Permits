import pandas as pd
import geopandas as gp
from shapely.geometry import Point
import random
import numpy as np

Ott = pd.read_csv('http://data.ottawa.ca/dataset/9603c5e9-7de6-49b4-b3a1-25c913badc36/resource/c069e186-0a00-4141-9339-aefa9ba8e314/download/address-points.csv')

geometry = [Point(xy) for xy in zip(Ott['POINT_X'],Ott['POINT_Y'])]
df = gp.GeoDataFrame(Ott,geometry=geometry)
df.crs = {'init' :'epsg:32189'}
df = df.to_crs({'init': 'epsg:4326'})

df['PropType'] = np.random.choice(['Aggregate','Single Family','Apartment Condo'],size=len(df))
df['Mkt_Value'] = np.random.uniform(200000,1000000,size=len(df)).astype(int)
df['Sqr_ft'] = np.random.uniform(400,3000,size=len(df)).astype(int)

def random_dates(start, end, n=10):

    start_u = start.value//10**9
    end_u = end.value//10**9

    return pd.to_datetime(np.random.randint(start_u, end_u, n), unit='s')

start = pd.to_datetime('2015-01-01')
end = pd.to_datetime('2019-09-01')
dates = random_dates(start, end,n=len(df))

df['Date'] = dates
df['Date']=df.Date.dt.date
df['Date'] = df['Date'].astype(str)

df = df.loc[:,['FULLADDR','PropType','Mkt_Value','Sqr_ft','Date','geometry']]



df.to_file('test.geojson',driver='GeoJSON')