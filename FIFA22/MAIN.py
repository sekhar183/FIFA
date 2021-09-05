#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from bs4 import BeautifulSoup
import requests
import pandas as pd
from tqdm import tqdm
import numpy as np
import time
import time
from tqdm import tqdm
from itertools import chain


# In[ ]:


DATA = pd.read_excel('../Cleaned_FIFA_players.xlsx', engine='openpyxl')


# In[ ]:


DATA=DATA[DATA['position']!='GK']
DATA['ref_url1']=DATA['ref_url'].apply(lambda x: 'https://www.fifplay.com/fifa-22/players'+str(x)[29:])


# ## Position & Info

# In[ ]:


found_url = []
not_found = []

df_position=pd.DataFrame()

for URL in tqdm(DATA['ref_url1'][:10000]):
    try:
        info_data=[]
        current_page=URL
        page = requests.get(current_page)
        soup = BeautifulSoup(page.content, "html.parser")
        card = soup.find('h4', attrs={'class':['text-uppercase margin-left-2px font-lighter']})
        
        table = soup.find('table', attrs={'class':['table table-details bg-white small']})
        table_body = table.find('tbody')
        rows = table_body.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            info_data.append([ele for ele in cols if ele])
        info_data=list(chain.from_iterable(info_data))
        info_data=info_data+[current_page] + [card.text]
        
        position_data = []
        table = soup.findAll('table', attrs={'class':['table table-details bg-white small']})[1]
        table_body = table.find('tbody')
        rows = table_body.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            position_data.append([ele for ele in cols if ele])
        position_data=list(chain.from_iterable(position_data))
        position_data=position_data+info_data
        
        pace_data=[]
        table = soup.findAll('table', attrs={'class':['table small']})[0]
        table_body = table.find('tbody')
        rows = table_body.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            pace_data.append([ele for ele in cols if ele])
        pace_data=list(chain.from_iterable(pace_data))
        pace_data=pace_data+position_data

        dribbling_data = []
        table = soup.findAll('table', attrs={'class':['table small']})[1]
        table_body = table.find('tbody')
        rows = table_body.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            dribbling_data.append([ele for ele in cols if ele])
        dribbling_data=list(chain.from_iterable(dribbling_data))
        dribbling_data=dribbling_data+pace_data

        shooting_data=[]
        table = soup.findAll('table', attrs={'class':['table small']})[2]
        table_body = table.find('tbody')
        rows = table_body.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            shooting_data.append([ele for ele in cols if ele])
        shooting_data=list(chain.from_iterable(shooting_data))
        shooting_data=shooting_data+dribbling_data

        defending_data=[]
        table = soup.findAll('table', attrs={'class':['table small']})[3]
        table_body = table.find('tbody')
        rows = table_body.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            defending_data.append([ele for ele in cols if ele])
        defending_data=list(chain.from_iterable(defending_data))
        defending_data=defending_data+shooting_data

        passing_data=[]
        table = soup.findAll('table', attrs={'class':['table small']})[4]
        table_body = table.find('tbody')
        rows = table_body.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            passing_data.append([ele for ele in cols if ele])
        passing_data=list(chain.from_iterable(passing_data))
        passing_data=passing_data+defending_data

        physical_data=[]
        table = soup.findAll('table', attrs={'class':['table small']})[5]
        table_body = table.find('tbody')
        rows = table_body.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            physical_data.append([ele for ele in cols if ele])
        physical_data=list(chain.from_iterable(physical_data))
        physical_data=physical_data+passing_data
        
        df_position = df_position.append(pd.DataFrame([physical_data]), ignore_index=True)
            
    except:
        not_found.append(URL)


# In[35]:


df_position.to_csv('all_attributes_1to10000.csv', header=True, index=False)


