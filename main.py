from flask import Flask, request, jsonify, render_template

# from joblib import dump, load
import logging
from flask.logging import create_logger

import pickle

import pandas as pd
  

app = Flask(__name__)
LOG = create_logger(app)
LOG.setLevel(logging.INFO)

@app.route("/")
def home():
    """Entry (main) route. Some functionality Explainations"""
    return render_template('main.html')

@app.route("/readme")
def readme():
    """Entry (main) route. Some functionality Explainations"""
    return render_template('README.html')


@app.route('/predict',methods=['POST'])
def predict():
    """ Predict route. Only Handles POST requests"""
    
    rfr = pickle.load(open('./model/predict.pickle', "rb"))
    med = pickle.load(open('./model/median.pickle', "rb"))

    json_payload =   request.json
 
    LOG.info("JSON payload: sucess ")

    X_score = pd.DataFrame(json_payload)
    X_score.fillna(med,inplace=True)
    predicted = rfr.predict_proba(X_score )[:,1]
    LOG.info("Prediction: sucess ")
    return jsonify({'predicted=1': list(predicted)})

if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='0.0.0.0', port=8080, debug=True)
