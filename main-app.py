from flask import Flask, escape, request, jsonify

from joblib import dump, load
import logging
from flask.logging import create_logger
import json

import pickle

import os
import pandas as pd
import numpy as np
# os.getcwd()


app = Flask(__name__)
LOG = create_logger(app)
LOG.setLevel(logging.INFO)

@app.route('/predict',methods=['POST'])
def predict():
   # name = request.args.get("name", "World")
   # return f'Hello, {escape(name)}!'

   tranformerX = pickle.load(open('transform_X.pickle', "rb"))
   tranformerY = pickle.load(open('transform_Y.pickle', "rb"))

   rfr = pickle.load(open('predict.pickle', "rb"))
   """
   test = pd.read_csv("test.csv")
   x_test = test.drop(['Unnamed: 0', 'mv'], axis=1)
   payload  =x_test[0:2].to_json()
   json_payload = json.loads(payload)
   """

   # json_payload =   json.loads(request.json)
   json_payload =   request.json

   LOG.info(f"JSON payload: %s {type(json_payload)}")

   df = pd.DataFrame(json_payload)
   transformed = tranformerX.transform(df)
   predict = rfr.predict(transformed )

   predict_transformed = tranformerY.inverse_transform(predict.reshape(-1,1)).flatten()
   return jsonify({'predict': list(predict_transformed)})

if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
