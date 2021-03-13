init = """
# Download files from Kaggle for ETL
# Note you must have kaggle's json credentials saved if you want to use this method. 
# Alternative is to go to Kaggle and download files directly.


# Instructions:

$ pip install kaggle 

# go to Kaggle account get your json credentials and save them in /<username>/.kaggle

$ python etl.py
"""
print(init, "\n")

from kaggle.api.kaggle_api_extended import KaggleApi
from zipfile import ZipFile
import os
import pandas as pd

api = KaggleApi()
api.authenticate()


# In[16]:
kaggle_comp = 'GiveMeSomeCredit'
print("Competition Name: ", kaggle_comp, "\n")

# In[23]:
print("Competition Files: ", api.competition_list_files(kaggle_comp), "\n")

# In[17]:
print("Download/Extract/Clean\n") 
api.competition_download_files(kaggle_comp)

# In[20]:

zf = ZipFile('GiveMeSomeCredit.zip')
zf.extractall('data/') #save files in selected folder
zf.close()
os.remove('GiveMeSomeCredit.zip')

# In[25]:

print("------------Printing sample------------\n")
print(pd.read_csv("./data/cs-test.csv").head().to_string())




