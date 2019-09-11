import pandas as pd
from bs4 import BeautifulSoup
import requests 

# Step 1 go through webpage  and get all the id's for historical data

webpage = requests.get('http://data.ottawa.ca/dataset/construction-demolition-pool-enclosure-permits-monthly')

soup = BeautifulSoup(webpage.text,'html.parser')
links = soup.find(class_='table table-striped').find_all('a',href=True)

OttPermits = pd.DataFrame(columns=['ST # ', 'ROAD', 'PC', 'WARD', 'PLAN', 'LOT', 'CONTRACTOR ',
       'BLG TYPE ', 'MUNICIPALITY ', 'DESCRIPTION', 'D.U.', 'VALUE', 'FT2',
       'PERMIT#', 'APPL. TYPE', 'ISSUED DATE'])

# Step 2 loop through links and grab historical data 
for link in links:
    if ((len(link['title'])) > 20) & (link['title'][-4:].strip() in(['2014','2015','2016'])):
        tempPage = requests.get('http://data.ottawa.ca'+link['href'])
        tempSoup = BeautifulSoup(tempPage.text,'html.parser')
        data = tempSoup.find(class_='muted ellipsis').find('a')['href']
        test= pd.read_excel(data,sheet_name=1)
        OttPermits = OttPermits.append(test,sort=False)
    elif ((len(link['title'])) > 20):
        tempPage = requests.get('http://data.ottawa.ca'+link['href'])
        tempSoup = BeautifulSoup(tempPage.text,'html.parser')
        data = tempSoup.find(class_='muted ellipsis').find('a')['href']
        test = pd.read_excel(data,sheet_name=0,header=5)
        OttPermits = OttPermits.append(test,sort=False)
    elif link['title'][-4:] == '2019':
        tempPage = requests.get('http://data.ottawa.ca'+link['href'])
        tempSoup = BeautifulSoup(tempPage.text,'html.parser')
        data = tempSoup.find(class_='muted ellipsis').find('a')['href']
        if link['title'][:3] in ['Feb','May','Jun']:
            test = pd.read_excel(data,sheet_name=0,header=5)
            OttPermits = OttPermits.append(test,sort=False)
        else:
            test = pd.read_excel(data,sheet_name=0,header=6)
            OttPermits = OttPermits.append(test,sort=False)

        
OttPermits = OttPermits.dropna(subset=['PERMIT#'])
OttPermits.to_excel('../Ignore/ottPermits.xlsx',index=False)



