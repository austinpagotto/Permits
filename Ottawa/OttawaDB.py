import os
import pandas as pd
from datetime import datetime
from pymongo import MongoClient
from credentials import connection


client = MongoClient(connection)
db = client['Address']['Ottawa']

Address = pd.read_excel('../Ignore/ottAddress0.xlsx')
for filename in os.listdir('../Ignore'):
    if filename[10] in ['1','2','3']:
        tempfile = pd.read_excel('../Ignore/'+filename)
        Address = Address.append(tempfile,sort=False)

Address = Address.to_dict(orient='records')

db.insert_many(Address)
# permits = pd.read_excel('../Ignore/ottPermits.xlsx')







# Clean up permits before geocoding
# permits = permits.loc[permits['DESCRIPTION'].astype(str).str[:5].str.upper() == 'CONST']


