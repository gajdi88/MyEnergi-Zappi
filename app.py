import pycharmpatch
from flask import Flask, request, render_template, redirect, url_for, session, abort, make_response
from flask_session import Session
import json
import os
import pandas as pd
from datetime import timedelta
import requests
from requests.auth import HTTPDigestAuth
from myenergi import Myenergi

app = Flask(__name__)


@app.route('/')
def index():
    mysession = Myenergi()
    statuses = mysession.summarize_statuses()
    return render_template('index.html', statuses=statuses)



if __name__ == '__main__':
    app.run(debug=True)