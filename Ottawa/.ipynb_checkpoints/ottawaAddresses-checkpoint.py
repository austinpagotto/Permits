import requests
import zipfile
import io
import os
import geopandas as gp
import pandas as pd
from shapely.geometry import Point 
import time

Address = pd.read_csv('http://data.ottawa.ca/dataset/9603c5e9-7de6-49b4-b3a1-25c913badc36/resource/c069e186-0a00-4141-9339-aefa9ba8e314/download/address-points.csv')

Current = pd.read_excel('../Ignore/ottAddress0.xlsx')
for filename in os.listdir('../Ignore'):
    if filename[10] in ['1','2','3']:
        tempfile = pd.read_excel('../Ignore/'+filename)
        Current = Current.append(tempfile,sort=False)

NewAddresses = Address.merge(Current.loc[:,['PI_MUNICIPAL_ADDRESS_ID']],left_on = 'PI_MUNICIPAL_ADDRESS_ID',right_on='PI_MUNICIPAL_ADDRESS_ID',how='left',indicator=True)
NewAddresses = NewAddresses.loc[NewAddresses['_merge']=='left_only'].drop(columns='_merge')

if len(NewAddresses) > 0:
    geometry = [Point(xy) for xy in zip(NewAddresses['POINT_X'],NewAddresses['POINT_Y'])]
    df = gp.GeoDataFrame(NewAddresses,geometry=geometry)
    start = time.time()
    df.crs = {'init' :'epsg:32189'}
    df = df.to_crs({'init': 'epsg:4326'})
    end = time.time()
    print(end-start)
    df['lat'] = df.geometry.y
    df['lon'] = df.geometry.x
    Current = Current.append(df,sort=False)
    Current.to_excel('../Ignore/ottAddress_Final.xlsx',index=False)


# INITAL Code for chunksize 

# addr = pd.read_csv('http://data.ottawa.ca/dataset/9603c5e9-7de6-49b4-b3a1-25c913badc36/resource/c069e186-0a00-4141-9339-aefa9ba8e314/download/address-points.csv',chunksize=100000)


# for i,chunk in enumerate(addr):
#     print(i)
#     geometry = [Point(xy) for xy in zip(chunk['POINT_X'],chunk['POINT_Y'])]
#     df = gp.GeoDataFrame(chunk,geometry=geometry)
#     start = time.time()
#     df.crs = {'init' :'epsg:32189'}
#     df = df.to_crs({'init': 'epsg:4326'})
#     end = time.time()
#     print(end-start)
#     df['lat'] = df.geometry.y
#     df['lon'] = df.geometry.x
#     df.to_excel('../Ignore/ottAddress'+str(i)+'.xlsx',index=False)










