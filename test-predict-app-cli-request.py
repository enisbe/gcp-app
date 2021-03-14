import sys, getopt
import mlib
import requests 
import json

url = "http://localhost:8080/predict"
url = "https://my-project-434-301711.uc.r.appspot.com/predict"
 
"""Reading arguments"""

opts, args = getopt.getopt(sys.argv[1:],"f:t:" )

 
args = dict(opts)

file = args['-f']
top = args['-t']
print("Reading from file: ", file)

# set the number of records to score
try:
    top=int(top)
except:
    top=None

 
payload = mlib.create_json_payload(mlib.load_test_data(file)[0:top])

results = mlib.request_payload(url,payload)

 
print('----Response Headers-----')
print(json.dumps(dict(results.headers),indent=4))
print("\n")
print(json.dumps(results.json(),indent=4))
 