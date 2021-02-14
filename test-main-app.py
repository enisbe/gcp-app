#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 14 05:04:10 2021

@author: ubuntu
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os
import pandas as pd
import numpy as np
import json
import requests, base64


os.getcwd()

# os.chdir("./gcp-app")


url = "http://127.0.0.1:8080/predict"
url = "https://my-project-434-301711.uc.r.appspot.com/predict"

test = pd.read_csv("./test.csv")


x_test = test.drop(['Unnamed: 0','mv'],axis=1)
y_test = test[['mv']]


# Small Requst
payload  =json.loads(x_test[0:10].to_json())
r = requests.post(url, json=payload)
r.json()

#Medim Request
payload  =json.loads(x_test.to_json())
r = requests.post(url, json=payload)
r.json()

def request_payload(url,payload):
    r = requests.post(url, json=payload)
    

#Medim Request
df = pd.concat([x_test]*200)
df = df.reset_index(drop=True)
payload  =json.loads(df.to_json())

%%time
r = requests.post(url, json=payload)
len(r.json()['predict'])

import sys
sys.executable

r

r.headers


r.content


r.json()


combine = {'actual': y_test[0:10]['mv'].tolist(),
          'predicted': r.json()['predict']}

pd.DataFrame(combine)
