#!/usr/bin/env python
# coding: utf-8

# In[135]:


from bs4 import BeautifulSoup
import requests
import pandas as pd
from tqdm import tqdm
import numpy as np
import time
from selenium import webdriver
import time
from tqdm import tqdm


# In[136]:


DATA = pd.read_excel('Cleaned_FIFA_players.xlsx', engine='openpyxl')


# In[137]:


DATA['ref_url']


# In[138]:


df=pd.DataFrame(columns=['ref_url', 'pace', 'shooting', 'passing', 'dribbling', 'defending', 'physical'])


# In[139]:


rating1 = 'main-stat-rating-title text-center fifa-green'
rating2 = 'main-stat-rating-title text-center fifa-light-green'
rating3 = 'main-stat-rating-title text-center fifa-red'
rating4 = 'main-stat-rating-title text-center fifa-yellow'


# In[140]:


options = webdriver.ChromeOptions()
options.add_argument("headless")
driver = webdriver.Chrome(executable_path=r'C:/Users/KANTE/webdriver/chromedriver.exe', chrome_options=options)


# In[146]:


i=0
for URL in tqdm(DATA['ref_url'][10001:], position=0):
    driver.get(URL)
    #time.sleep(2)
    if i==0:
        driver.find_element_by_xpath('/html/body/div[8]/div[2]/div[2]/div[2]/div[3]/input').click()
    i+=1
    page=driver.execute_script("return document.body.innerHTML;")
    soup = BeautifulSoup(page, "html.parser")
    ratings=soup.findAll('div',{'class':[rating1,rating2,rating3,rating4]})
    pl_ratings=[]
    pl_ratings.append(URL)
    for rating in ratings:
        pl_ratings.append(int(rating.text))
    df = df.append(pd.DataFrame([pl_ratings], columns=df.columns), ignore_index=True)


# In[ ]:


driver.close()


# In[147]:


df.to_csv("FIFA_21_1001to.csv",index=False, header=True)
df.to_excel("FIFA_21_1001to.excel",index=False, header=True)





