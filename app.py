from flask import Flask, request
import json 
import random
import requests
import datetime
import os
from dateutil.parser import parse
app = Flask(__name__)
app.debug = True

@app.route('/')
def hello():
    return '{"Hello": "World!"}'

@app.route('/webhook',methods=['POST'])
def index():
    #Get the geo-city entity from the dialogflow fullfilment request.
    body = request.json()
    dep_city= body['queryResult']['parameters']['dep']
    
    appId = 'c29d8e653315ba18a7491286b9d6157b'

    #Connect to the API to get IATA Codes
    api_url = "http://api.aviationstack.com/v1/cities?access_key=" + appId + "&search=" + dep_city
    headers = {'Content-Type': 'application/json'} #Set the HTTP header for the API request
    response = requests.get(api_url, headers=headers) #Connect to flightlab and read the JSON response.
    iata=response.json() #Convert the JSON string to a dict for easier parsing.
    dep_iata = str(iata[0]["iata_code"])

    #build the Dialogflow reply.
    reply = '{"fulfillmentMessages": [ {"text": {"text": ["IATA Code of Airport is '+ dep_iata + '"] } } ]}'
    return reply

test_mode = 0
port = int(os.environ.get("PORT", 5000))

if __name__ == "main":
    if test_mode == 1:
        app.run(debug=False, host='0.0.0.0', port=port)
    else:
        app.run(debug=True, use_reloader=True, host='0.0.0.0', port=port)
