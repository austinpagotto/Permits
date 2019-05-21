import requests
import zipfile
import io
import geopandas as gp
import pandas as pd
from shapely.geometry import Point 
import pyproj
pyproj.Proj("+init=epsg:4326")

addr = pd.read_csv('http://data.ottawa.ca/dataset/9603c5e9-7de6-49b4-b3a1-25c913badc36/resource/c069e186-0a00-4141-9339-aefa9ba8e314/download/address-points.csv')
geometry = [Point(xy) for xy in zip(addr['POINT_X'],addr['POINT_Y'])]
addr = gp.GeoDataFrame(addr,geometry=geometry)
addr.crs = {'init' :'epsg:32189'}
addr = addr.to_crs({'init': 'epsg:4326'})









