import os

import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("TICKETMASTER_API_KEY")

url = "https://app.ticketmaster.com/discovery/v2/events.json"

states = ["OH", "MI", "IN", "KY", "PA", "WV"]

for state in states:
    params = {
        "apikey": api_key,
        "countryCode": "US",
        "stateCode": state,
        "size": 10,
    }

    response = requests.get(url, params=params)

    print(f"\n{state} - Status: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        events = data.get("_embedded", {}).get("events", [])

        print(f"Found {len(events)} events.")

        for event in events:
            print(event["name"])
    else:
        print(response.text)