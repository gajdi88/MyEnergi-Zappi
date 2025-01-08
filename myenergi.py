import json
import os
import pandas as pd
from datetime import timedelta
import requests
from requests.auth import HTTPDigestAuth


class Myenergi:

    def __init__(self):
        self.apikeys = self.load_api_keys()
        self.sessions = self.connect_session()
        self.statuses = self.get_status_updates()


    def load_api_keys(self):
        # load apikeys.csv where columns are: serial, apikey
        apikeys = pd.read_csv('apikeys.csv')
        return apikeys

    def connect_session(self):
        sessions = []

        for serial, apikey in zip(self.apikeys['serial'], self.apikeys['apikey']):
            sessions.append(self.apiconnect(serial, apikey))

        return sessions

    def apiconnect(self, serial, apikey):
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

    def get_status_updates(self):
        statuses = []
        base_url = "https://s18.myenergi.net"
        for tsession in self.sessions:
            # response = session.get(f"{base_url}/test-endpoint")
            response = tsession.get(f"{base_url}/cgi-jstatus-Z")
            response.raise_for_status()  # Raise an exception for bad status
            json_resp = response.json()
            status = json_resp['zappi'][0]
            statuses.append(status)
            # decipher response.content from JSON
        return statuses

    def summarize_statuses(self):
        summarized_statuses = []
        for idx, status in enumerate(self.statuses):
            pst = status.get("pst", "N/A")
            sta = status.get("sta", "N/A")
            summary = ""

            if pst == "A":
                summary = "EV Disconnected"
                color = "gray"
            elif pst == "C2":
                summary = "Charging"
                color = "green"
            elif pst in ["B2", "C1"] and sta != 5:
                summary = "EV Ready to Charge"
                color = "yellow"
            elif sta == 5:
                summary = "Charging Complete"
                color = "blue"
            elif pst == "F":
                summary = "Fault"
                color = "red"
            else:
                summary = "Unknown Status"
                color = "orange"

            total_charge = (status.get('gen', 0) + status.get('grd', 0)) / 1000
            total_charge = round(total_charge, 1)  # Round to 1 decimal place
            summarized_statuses.append({
                "charger": f"Charger {idx + 1}",
                "status": summary,
                "color": color,
                "total_charge": total_charge,
                "details": status
            })
        return summarized_statuses
