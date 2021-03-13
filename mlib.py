import pandas as pd
import json
import requests
import pickle


keep =   ['RevolvingUtilizationOfUnsecuredLines', 'age', 'NumberOfTime30-59DaysPastDueNotWorse', 'DebtRatio', 'MonthlyIncome', 'NumberOfOpenCreditLinesAndLoans', 'NumberOfTimes90DaysLate', 'NumberRealEstateLoansOrLines', 'NumberOfTime60-89DaysPastDueNotWorse', 'NumberOfDependents']

def load_test_data(file):    
    test = pd.read_csv(f"{file}")
    x_test = test[keep]
    return x_test 


def create_json_payload(df):
    payload   =json.loads(df.to_json())
    return payload
    
    
def request_payload(url,payload):    
    r = requests.post(url, json=payload)
    return r 

def load_models():
    rfr = pickle.load(open('./model/predict.pickle', "rb"))
    med = pickle.load(open('./model/median.pickle', "rb"))
    return rfr, med

def multiply(a,b):
    """Just some fake function for testing check"""
    return a*b