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


url = "http://localhost:8080/predict"
url = "https://my-project-434-301711.uc.r.appspot.com/predict"


def  test_data():
    
    test = pd.read_csv("./test.csv")
    x_test = test.drop(['Unnamed: 0','mv'],axis=1)
    y_test = test[['mv']]
    return x_test, y_test

def request_payload(url,payload):
    len_r = len(payload['crim'])
    print(len_r)
    r = requests.post(url, json=payload)
    len_return = len(r.json()['predict'])
    print("Request made at: ", url)
    print("Length of request: ", len_r, "; Lenght of return: ", len_return)
    return r.json()



x_test, y_test = test_data()


# Small Requst
payload_small  =json.loads(x_test[0:10].to_json())
#Medim Request
payload_medium  =json.loads(x_test.to_json())
#Medim Request
df = pd.concat([x_test]*200)
df = df.reset_index(drop=True)
payload_large  =json.loads(df.to_json())




url = "http://localhost:8080/predict"
url = "https://my-project-434-301711.uc.r.appspot.com/predict"



%%time
results = request_payload(url, payload_small)
%%time
results = request_payload(url, payload_medium)
%%time
results = request_payload(url, payload_large)

r

r.headers


r.content


r.json()


combine = {'actual': y_test[0:10]['mv'].tolist(),
          'predicted': r.json()['predict']}

pd.DataFrame(combine)
