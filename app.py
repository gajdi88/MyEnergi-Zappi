import pycharmpatch
from flask import Flask, request, render_template, redirect, url_for, session, abort, make_response
from flask_session import Session
import json
import os
import pandas as pd
from datetime import timedelta
import requests
from requests.auth import HTTPDigestAuth

app = Flask(__name__)


@app.route('/')
def index():
    apikeys = load_api_keys()
    sessions = connect_session(apikeys)
    statuses = get_status_updates(sessions)
    print(statuses)
    return render_template('index.html')


def load_api_keys():
    # load apikeys.csv where columns are: serial, apikey
    apikeys = pd.read_csv('apikeys.csv')
    return apikeys

def connect_session(apikeys):
    sessions = []

    for serial, apikey in zip(apikeys['serial'], apikeys['apikey']):
        sessions.append(apiconnect(serial, apikey))

    return sessions

def apiconnect(serial, apikey):
    # Base URL for the API
    base_url = "https://s18.myenergi.net"

    # Create a session object to maintain the connection
    session = requests.Session()

    # Configure digest authentication
    session.auth = HTTPDigestAuth(serial, apikey)

    session.headers.update({
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    })

    return session

def get_status_updates(sessions):
    statuses = []
    base_url = "https://s18.myenergi.net"
    for tsession in sessions:
        # response = session.get(f"{base_url}/test-endpoint")
        response = tsession.get(f"{base_url}/cgi-jstatus-Z")
        response.raise_for_status()  # Raise an exception for bad status
        json_resp = response.json()
        status = json_resp['zappi'][0]
        statuses.append(status)
        # decipher response.content from JSON
    return statuses

if __name__ == '__main__':
    app.run(debug=True)