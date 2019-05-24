import requests
import zipfile
import io
import geopandas as gp
import pandas as pd
from shapely.geometry import Point 
import time

# read in new addres data and old address data, append and change coordinates for any new addresses
addr = pd.read_csv('http://data.ottawa.ca/dataset/9603c5e9-7de6-49b4-b3a1-25c913badc36/resource/c069e186-0a00-4141-9339-aefa9ba8e314/download/address-points.csv',chunksize=100000)


for i,chunk in enumerate(addr):
    print(i)
    geometry = [Point(xy) for xy in zip(chunk['POINT_X'],chunk['POINT_Y'])]
    df = gp.GeoDataFrame(chunk,geometry=geometry)
    start = time.time()
    df.crs = {'init' :'epsg:32189'}
    df = df.to_crs({'init': 'epsg:4326'})
    end = time.time()
    print(end-start)
    df['lat'] = df.geometry.y
    df['lon'] = df.geometry.x
    df.to_excel('../Ignore/ottAddress'+str(i)+'.xlsx',index=False)










