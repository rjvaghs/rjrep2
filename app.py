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
    arr_city= body['queryResult']['parameters']['arr']
    flight_date= body['queryResult']['parameters']['flight_date'][0]
    date = datetime.datetime.strptime(flight_date,'%Y-%m-%dT%H-%M-%S-%f%z')
    flight_date = date.strftime('%Y-%m-%d')

    appId = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI0IiwianRpIjoiZTcyNWNlOGRhYjg3NTA0YTlhY2Q0OGM0MDMyYmNkODk3M2RiZTBiYmExMWQ1MDI3OWIxNzNkYjA1NmUyMGM4NWU2YzEwYWIxMjc1ODBmNGYiLCJpYXQiOjE2NjU2MDkyNDIsIm5iZiI6MTY2NTYwOTI0MiwiZXhwIjoxNjk3MTQ1MjQxLCJzdWIiOiIxNDkyNCIsInNjb3BlcyI6W119.m_32z-sDadzteKBWVArGhej-7PS2Cv7bDJ_MEFVA2_lwLFUHdGyLa9xsbu2921Wb28fUaBAjkVyT7dA0BhlkAQ'

    #Connect to the API to get IATA Codes
    api_url1 = "https://app.goflightlabs.com/cities?access_key=" + appId + "&city_name=" + dep_city
    headers = {'Content-Type': 'application/json'} #Set the HTTP header for the API request
    response = requests.get(api_url1, headers=headers) #Connect to flightlab and read the JSON response.
    iata=response.json() #Convert the JSON string to a dict for easier parsing.
    dep_iata = str(iata["data"][0]["iata_code"])

    api_url2 = "https://app.goflightlabs.com/cities?access_key=" + appId + "&city_name=" + arr_city
    headers = {'Content-Type': 'application/json'} #Set the HTTP header for the API request
    response = requests.get(api_url2, headers=headers) #Connect to flightlab and read the JSON response.
    iata2=response.json() #Convert the JSON string to a dict for easier parsing.
    arr_iata = str(iata2["data"][0]["iata_code"])
    
    #Connect to the API and get the JSON file.
    api_url="https://app.goflightlabs.com/flights?access_key=" + appId + "&dep_iata=" + dep_iata + "&arr_iata=" + arr_iata + "&flight_date=" + flight_date
    headers = {'Content-Type': 'application/json'} #Set the HTTP header for the API request
    response = requests.get(api_url, headers=headers) #Connect to openweather and read the JSON response.
    r=response.json() #Conver the JSON string to a dict for easier parsing.

    #Extract real-time flight data we want from the dictionery and convert to strings to make it easy to generate the dialogflow reply.
    
    dep_airport = str(r["data"][0]["departure"]["airport"])
    arr_airport = str(r["data"][0]["arrival"]["airport"])
    airline = str(r["data"][0]["airline"]["name"])
    flight_no = str(r["data"][0]["flight"]["number"])
    scheduled_dep = str(r["data"][0]["departure"]["scheduled"])
    scheduled_arr = str(r["data"][0]["arrival"]["scheduled"])
    get_date_obj = parse(str(scheduled_dep))
    scheduled_dep_time = str(get_date_obj.strftime('%Y-%m-%d %H:%M:%S'))

    #build the Dialogflow reply.
    reply = '{"fulfillmentMessages": [ {"text": {"text": ["Flight from '+ dep_airport + ' to '+ arr_airport + ' is scheduled on ' + scheduled_dep_time + ' with ' + airline + ' and flight number ' + flight_no +'"] } } ]}'
    return reply

test_mode = 0
port = int(os.environ.get("PORT", 5000))

if __name__ == "main":
    if test_mode == 1:
        app.run(debug=False, host='0.0.0.0', port=port)
    else:
        app.run(debug=True, use_reloader=True, host='0.0.0.0', port=port)

print("hi")
