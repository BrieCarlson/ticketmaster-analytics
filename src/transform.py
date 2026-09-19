import json
import os

import pandas as pd

INPUT_FILE = "data/raw_events.json"
OUTPUT_FILE = "data/events_clean.csv"


def get_primary_classification(event):
    classifications = event.get("classifications", [])

    for classification in classifications:
        if classification.get("primary"):
            return classification

    return classifications[0] if classifications else {}


def transform_event(event):
    classification = get_primary_classification(event)

    segment = classification.get("segment", {})
    genre = classification.get("genre", {})
    subgenre = classification.get("subGenre", {})

    embedded = event.get("_embedded", {})

    venues = embedded.get("venues", [])
    attractions = embedded.get("attractions", [])

    venue = venues[0] if venues else {}
    attraction = attractions[0] if attractions else {}

    venue_city = venue.get("city", {})
    venue_state = venue.get("state", {})
    location = venue.get("location", {})

    price_ranges = event.get("priceRanges", [])
    price_range = price_ranges[0] if price_ranges else {}

    dates = event.get("dates", {})
    start = dates.get("start", {})

    return {
        "event_id": event.get("id"),
        "event_name": event.get("name"),
        "event_url": event.get("url"),
        "event_date": start.get("localDate"),
        "event_time": start.get("localTime"),
        "timezone": dates.get("timezone"),
        "event_status": dates.get("status", {}).get("code"),
        "state": venue_state.get("stateCode") or event.get("_source_state"),
        "city": venue_city.get("name"),
        "venue_id": venue.get("id"),
        "venue_name": venue.get("name"),
        "latitude": location.get("latitude"),
        "longitude": location.get("longitude"),
        "segment": segment.get("name"),
        "genre": genre.get("name"),
        "subgenre": subgenre.get("name"),
        "attraction_id": attraction.get("id"),
        "attraction_name": attraction.get("name"),
        "promoter": event.get("promoter", {}).get("name"),
        "price_min": price_range.get("min"),
        "price_max": price_range.get("max"),
        "currency": price_range.get("currency"),
    }


def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        raw_events = json.load(file)

    clean_events = [transform_event(event) for event in raw_events]

    df = pd.DataFrame(clean_events)

    original_count = len(df)

    df = df.drop_duplicates(subset="event_id")

    duplicates_removed = original_count - len(df)

    os.makedirs("data", exist_ok=True)

    df.to_csv(OUTPUT_FILE, index=False)

    print(f"Saved {len(df)} cleaned events to {OUTPUT_FILE}")
    print(f"Duplicates removed: {duplicates_removed}")
    print(f"Columns: {len(df.columns)}")
    print("\nColumns:")
    print(", ".join(df.columns))

    print("\nFirst 5 events:")
    print(df.head().to_string(index=False))


if __name__ == "__main__":
    main()