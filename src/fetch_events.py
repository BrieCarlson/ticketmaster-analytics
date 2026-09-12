import os
import json

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TICKETMASTER_API_KEY")
URL = "https://app.ticketmaster.com/discovery/v2/events.json"

STATES = ["OH", "MI", "IN", "KY", "PA", "WV"]
EVENTS_PER_STATE = 200


def fetch_events(state):
    events = []
    page = 0

    while len(events) < EVENTS_PER_STATE:
        params = {
            "apikey": API_KEY,
            "countryCode": "US",
            "stateCode": state,
            "size": 200,
            "page": page,
        }

        response = requests.get(URL, params=params)

        if response.status_code != 200:
            print(f"{state}: API error {response.status_code}")
            print(response.text)
            break

        data = response.json()
        page_events = data.get("_embedded", {}).get("events", [])

        if not page_events:
            break

        events.extend(page_events)

        total_pages = data.get("page", {}).get("totalPages", 0)

        print(
            f"{state}: fetched {len(events)} events "
            f"(page {page + 1}/{total_pages})"
        )

        if page + 1 >= total_pages:
            break

        page += 1

    return events[:EVENTS_PER_STATE]


def main():
    all_events = []

    for state in STATES:
        print(f"\nFetching {state}...")
        events = fetch_events(state)

        for event in events:
            event["_source_state"] = state

        all_events.extend(events)

    os.makedirs("data", exist_ok=True)

    with open("data/raw_events.json", "w", encoding="utf-8") as file:
        json.dump(all_events, file, indent=2)

    print(f"\nDone. Saved {len(all_events)} events to data/raw_events.json")


if __name__ == "__main__":
    main()