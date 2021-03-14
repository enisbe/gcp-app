#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 14 05:04:10 2021

@author: ubuntu
"""
import mlib
import requests 
import json

url = "http://localhost:8080/predict"
# url = "https://my-project-434-301711.uc.r.appspot.com/predict"

"""Reading arguments"""


file = "./data/cs-test.csv"
top = 10

payload = mlib.create_json_payload(mlib.load_test_data(file)[0:top])
# payload = mlib.create_json_payload(mlib.load_test_data(file)[1:2])

results = mlib.request_payload(url,payload)
 
print('----Response Headers-----')
print(json.dumps(dict(results.headers),indent=4))
print("\n")
print(json.dumps(results.json(),indent=4))
 