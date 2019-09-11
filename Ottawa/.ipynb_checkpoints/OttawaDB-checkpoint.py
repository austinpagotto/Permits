import os
import pandas as pd
from datetime import datetime
from pymongo import MongoClient
from credentials import connection

# Establish Connection
client = MongoClient(connection)
# Connect to Ottawa Address Database
db = client['Address']['Ottawa']
# Only add the new Addresses
Address = pd.read_excel('../Ignore/ottAddress_Final.xlsx')

# for filename in os.listdir('../Ignore'):
#     if filename[10] in ['1','2','3']:
#         tempfile = pd.read_excel('../Ignore/'+filename)
#         Address = Address.append(tempfile,sort=False)

# Get Addresses already in DB
Current = pd.DataFrame.from_records(db.find())
# join to isolate only new Addresses
NewAddresses = Address.merge(Current.loc[:,['PI_MUNICIPAL_ADDRESS_ID']],left_on = 'PI_MUNICIPAL_ADDRESS_ID',right_on='PI_MUNICIPAL_ADDRESS_ID',how='left',indicator=True)
NewAddresses = NewAddresses.loc[NewAddresses['_merge']=='left_only'].drop(columns='_merge')
# change format to be uploaded into DB
print(NewAddresses.info())
NewAddresses = NewAddresses.to_dict(orient='records')
# If there are any new addresses add them
if len(NewAddresses) > 0:
        db.insert_many(NewAddresses)

# Same logic as above! but for Permits
db = client['Permits']['Ottawa']
Permits = pd.read_excel('../Ignore/ottPermits.xlsx')
Permits.columns = Permits.columns.str.replace('.','')
Current = pd.DataFrame.from_records(db.find())

NewPermits = Permits.merge(Current.loc[:,['PERMIT#']],left_on = 'PERMIT#',right_on='PERMIT#',how='left',indicator=True)
NewPermits = NewPermits.loc[NewPermits['_merge']=='left_only'].drop(columns='_merge')
print(NewPermits.info())
NewPermits = NewPermits.to_dict(orient='records')

if len(NewPermits) > 0:
        db.insert_many(NewPermits)






