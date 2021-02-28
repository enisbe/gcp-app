from flask import Flask, request, jsonify

# from joblib import dump, load
import logging
from flask.logging import create_logger

import pickle

import pandas as pd
# os.getcwd()

app = Flask(__name__)
LOG = create_logger(app)
LOG.setLevel(logging.INFO)

@app.route("/")
def home():
    html = "<h3>Intro Page for prediction. Score model using /predict route</h3>"
    return html.format(format)


@app.route('/predict',methods=['POST'])
def predict():
   # name = request.args.get("name", "World")
   # return f'Hello, {escape(name)}!'

    tranformerX = pickle.load(open('transform_X.pickle', "rb"))
    tranformerY = pickle.load(open('transform_Y.pickle', "rb"))

    rfr = pickle.load(open('predict.pickle', "rb"))
    
    # test = pd.read_csv("test.csv")
    # x_test = test.drop(['Unnamed: 0', 'mv'], axis=1)
    # payload  =x_test[0:2].to_json()
    # json_payload = json.loads(payload)
    
   # json_payload =   json.loads(request.json)
    json_payload =   request.json
 
    LOG.info("JSON payload: %s " , type(json_payload) )

    df = pd.DataFrame(json_payload)
    transformed = tranformerX.transform(df)
    predicted = rfr.predict(transformed )

    predict_transformed = tranformerY.inverse_transform(predicted.reshape(-1,1)).flatten()
    return jsonify({'predict': list(predict_transformed)})

if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='0.0.0.0', port=8080, debug=True)
