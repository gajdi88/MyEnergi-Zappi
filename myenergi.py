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

    def display(self):
        statuses = self.statuses
        for idx, status in enumerate(statuses):
            print(f"Status {idx + 1}:")
            print(f"  Generated Watts (gen): {status.get('gen', 'N/A')}")
            print(f"  Watts from Grid (grd): {status.get('grd', 'N/A')}")
            print(f"  Power State (pst): {status.get('pst', 'N/A')} "
                  f"({'EV Disconnected' if status.get('pst') == 'A' else ''}"
                  f"{'EV Connected' if status.get('pst') == 'B1' else ''}"
                  f"{'Waiting for EV' if status.get('pst') == 'B2' else ''}"
                  f"{'EV Ready to Charge' if status.get('pst') == 'C1' else ''}"
                  f"{'Charging' if status.get('pst') == 'C2' else ''}"
                  f"{'Fault' if status.get('pst') == 'F' else ''})")
            print(f"  Status (sta): {status.get('sta', 'N/A')} "
                  f"({'Paused' if status.get('sta') == 1 else ''}"
                  f"{'Diverting/Charging' if status.get('sta') == 3 else ''}"
                  f"{'Complete' if status.get('sta') == 5 else ''})")
            total_charge = status.get('gen', 0) + status.get('grd', 0)
            print(f"  Total Charge (gen + grd): {total_charge}")
            print("-" * 40)

