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
    body = request.json
    dep_city= body['queryResult']['parameters']['dep']

    appId = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI0IiwianRpIjoiZTcyNWNlOGRhYjg3NTA0YTlhY2Q0OGM0MDMyYmNkODk3M2RiZTBiYmExMWQ1MDI3OWIxNzNkYjA1NmUyMGM4NWU2YzEwYWIxMjc1ODBmNGYiLCJpYXQiOjE2NjU2MDkyNDIsIm5iZiI6MTY2NTYwOTI0MiwiZXhwIjoxNjk3MTQ1MjQxLCJzdWIiOiIxNDkyNCIsInNjb3BlcyI6W119.m_32z-sDadzteKBWVArGhej-7PS2Cv7bDJ_MEFVA2_lwLFUHdGyLa9xsbu2921Wb28fUaBAjkVyT7dA0BhlkAQ'

    #Connect to the API to get IATA Codes
    api_url = "https://app.goflightlabs.com/cities?access_key=" + appId + "&city_name=" + dep_city
    headers = {'Content-Type': 'application/json'} #Set the HTTP header for the API request
    response = requests.get(api_url, headers=headers) #Connect to flightlab and read the JSON response.
    iata=response.json() #Convert the JSON string to a dict for easier parsing.
    dep_iata = str(iata["data"][0]["iata_code"])

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
