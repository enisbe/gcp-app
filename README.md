# GCP ML application Deployment 
----
    
###  Predicting the Probability of default -"GiveMeSomeCredit" ([Kaggle competition]('http://google.com'))
    
This application provides REST API prediction app that returns the probabability of default given the customer credit charterticis. 

Current the only enabled route is  @/predict and the only POST request are served to the client
    
The client can be anything  The application is agnostic to the languest (python/java/curl etc) as the data is served and handled using json data structure  
    
## Testing the application
    
#### 1. Locally
    
To start using the app the following procedure should be taked:
    
 
```bash 
$ python3 -m venv ~/.gcp-app
$ source ~/.gcp-app/bin/activate
```
    
After getting virtualenv set up download the data and test it locally

```bash
$ cd ~
$ git clone https://github.com/enisbe/gcp-app.git
$ cd gcp-app
$ git checkout test
$ make install
```

and start the app locally
    
```bash
python main.py
 * Serving Flask app "main" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 160-285-640
 * Running on http://0.0.0.0:8080/ (Press CTRL+C to quit)
```
    
Main route [http://localhost:8080/](http://localhost:8080) provides the basic information about the model 
    
#### 2. Deploy in GCP app-engine
    
Application can be deployed in Google Cloud using App Engine. In googleshell clone the directory from github and switch to prod (or test) branch:

```bash
$ git clone https://github.com/enisbe/gcp-app.git
$ cd gcp-app
$ git checkout prod
$ gcloud app create
$ gcloud app deploy app.yaml  --project [project name]

```
     
## Interaction with the application and making requests

There are many way that a client can make request:
    
1. ***Using python CLI*** (or any other languence) locally or remotely
2. ***Usuing Ipython*** or some other interactive shell 
3. ***Using curl*** or some other tool like curl (what is CURL?)

    
#### 1. Using Python CLI
    
Making requestion in local or remote enviroment is the same using python terminal. The only diffrence is where the request is routed. For testing locally open file `test-predict-app-cli-request.py` and uncomment `url = "http://localhost:8080/predict"` code line. For making requestion to the gcp app uncomment `url = "https://my-project-434-301711.uc.r.appspot.com/predict"`
    
Then the request can be python via python cli. If we are requesting from localhost then the command and response will look as follows: 

```bash
$ python test-predict-app-cli-request.py  -f ./data/cs-test.csv -t 10
Reading from file:  ./data/cs-test.csv
----Response Headers-----
{
    "Content-Type": "application/json",
    "Content-Length": "288",
    "Server": "Werkzeug/1.0.1 Python/3.8.8",
    "Date": "Sun, 14 Mar 2021 02:24:22 GMT"
}
{
    "predicted=1": [
        0.08020394910646916,
        0.041356749003717067,
        0.01543703769387024,
        0.07310729402770287,
        0.10729297692992816,
        0.025973690929737003,
        0.05397958700198282,
        0.04371209879083955,
        0.007954856044590747,
        0.40790066865922325
    ]
}
```
Sending the request to GCP app-engine using the same command:
    
``` bash
$ python test-predict-app-cli-request.py  -f ./data/cs-test.csv -t 10
Reading from file:  ./data/cs-test.csv
----Response Headers-----
{
    "Content-Type": "application/json",
    "Vary": "Accept-Encoding",
    "Content-Encoding": "gzip",
    "X-Cloud-Trace-Context": "6888a65914c443ec170d4c6c6b3bdc9e;o=1",
    "Date": "Sun, 14 Mar 2021 02:26:16 GMT",
    "Server": "Google Frontend",
    "Cache-Control": "private",
    "Alt-Svc": "h3-29=\":443\"; ma=2592000,h3-T051=\":443\"; ma=2592000,h3-Q050=\":443\"; ma=2592000,h3-Q046=\":443\"; ma=2592000,h3-Q043=\":443\"; ma=2592000,quic=\":443\"; ma=2592000; v=\"46,43\"",
    "Transfer-Encoding": "chunked"
}
{
    "predicted=1": [
        0.08020394910646918,
        0.041356749003717067,
        0.015437037693870236,
        0.07310729402770287,
        0.10729297692992816,
        0.025973690929737003,
        0.05397958700198282,
        0.04371209879083955,
        0.007954856044590746,
        0.40790066865922325
    ]
}
```    
**-f** argument indicates the file name<br>
**-t** aragument indicates how many rows to evaluate (all or any string would sned all rows to the server for scoring)

#### 2. Using Interactive Python
    
Using Inteative Python is straing forward. The code to test application and make request is found in `test-predict-app-kernel.py`

```Python 
"""This code can be run in interactive shell"""
import mlib
import requests 
import json

url = "http://localhost:8080/predict"
# url = "https://my-project-434-301711.uc.r.appspot.com/predict"

file = "./data/cs-test.csv"
top = 10

payload = mlib.create_json_payload(mlib.load_test_data(file)[0:top])

results = mlib.request_payload(url,payload)
 
print('----Response Headers-----')
print(json.dumps(dict(results.headers),indent=4))
print("\n")
print(json.dumps(results.json(),indent=4))
  
```
    
#### 3. Using curl

```bash 
$ ./curl-request.sh
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   468  100    52  100   416    192   1540 --:--:-- --:--:-- --:--:--  1733
{
  "predicted=1": [
    0.041356749003717067
  ]
}
 
```

### Model
    
* The model is based on the Kaggle competiion dataset used for "GiveMeSomeCredit" competition. The competition main page is found here <a href='https://www.kaggle.com/c/GiveMeSomeCredit/overview'>here</a>.
* `etl.py` can be used to automate the etl to extract the data and save in the local enviroment 
* Model training can be found in the `notebooks/train-credit.ipynb` 
* I used `scikit-learn` Random Forecast Classifier with GridSearchCV method to find the best fitting model
* The highst rank model in the competition had a score of 0.86. My model RFC Kaggle score was 0.859    

Test and Train AUC curves and results:

<img src="/static/images/prediction.png" alt="Test Data Prediction"> 

    
## Application Pipeline and Architecture

* This application deploys the Machine Learning in the Google Cloud enviorment and provides REST API interface that client can interact with it. The use case for such application is a model problem that potential has a broad user group that want to laverge the ML model application.  
    
* The application is built in Python using Flask web framework and it was deployed in GCP app engine. `Github actions` For Continous Integration (CI). For contieous deployment (CD) a trigger in GCP was created to track the `prod` in Github. On any change in the prod branch GCP app-engine redeploy the application. 

    
* The applicaiton was developed and tested locally. After sucessful testing the pushing to `test` branch repo where CI was used with linting and testing was used to ensure the application integration. Ooptionally, for senstivite projects, a CD with another app-engine can be deployed to respond to any change in `test`. For this application this was applied. After successul CI integration, `test` branch is merged with `prod` which is redoployed via GCP CD trigger. 

The ML app pipeline is shown blow: 

<img src="/static/images/application-pipeline-medium.png" alt="Application Pipeline"> 
