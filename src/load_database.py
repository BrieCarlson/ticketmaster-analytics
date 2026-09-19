import os
from datetime import date

import pandas as pd
import psycopg2
from dotenv import load_dotenv


load_dotenv()

CSV_FILE = "data/events_clean.csv"

DB_CONFIG = {
    "host": "localhost",
    "database": "ticketmaster_analytics",
    "user": "postgres",
    "password": os.getenv("DB_PASSWORD"),
    "port": 5432,
}

if not DB_CONFIG["password"]:
    raise ValueError("DB_PASSWORD is missing from .env")


def clean_value(value):
    """Convert pandas missing values to Python None."""
    return None if pd.isna(value) else value


def main():
    df = pd.read_csv(CSV_FILE)

    # The date this pipeline run represents.
    snapshot_date = date.today()

    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # VENUES
    venues = df[
        [
            "venue_id",
            "venue_name",
            "city",
            "state",
            "latitude",
            "longitude",
        ]
    ].dropna(subset=["venue_id"])

    venues = venues.drop_duplicates(subset="venue_id")

    for _, row in venues.iterrows():
        cursor.execute(
            """
            INSERT INTO venues (
                venue_id,
                venue_name,
                city,
                state,
                latitude,
                longitude
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (venue_id)
            DO UPDATE SET
                venue_name = EXCLUDED.venue_name,
                city = EXCLUDED.city,
                state = EXCLUDED.state,
                latitude = EXCLUDED.latitude,
                longitude = EXCLUDED.longitude;
            """,
            (
                clean_value(row["venue_id"]),
                clean_value(row["venue_name"]),
                clean_value(row["city"]),
                clean_value(row["state"]),
                clean_value(row["latitude"]),
                clean_value(row["longitude"]),
            ),
        )

    # ATTRACTIONS
    attractions = df[
        [
            "attraction_id",
            "attraction_name",
        ]
    ].dropna(subset=["attraction_id"])

    attractions = attractions.drop_duplicates(subset="attraction_id")

    for _, row in attractions.iterrows():
        cursor.execute(
            """
            INSERT INTO attractions (
                attraction_id,
                attraction_name
            )
            VALUES (%s, %s)
            ON CONFLICT (attraction_id)
            DO UPDATE SET
                attraction_name = EXCLUDED.attraction_name;
            """,
            (
                clean_value(row["attraction_id"]),
                clean_value(row["attraction_name"]),
            ),
        )

        # CURRENT EVENTS TABLE
        current_event_ids = set(df["event_id"].dropna())

        if current_event_ids:
            placeholders = ", ".join(["%s"] * len(current_event_ids))

            cursor.execute(
                f"""
                DELETE FROM events
                WHERE event_id NOT IN ({placeholders});
                """,
                tuple(current_event_ids),
            )

        for _, row in df.iterrows():
            values = (
                clean_value(row["event_id"]),
                clean_value(row["event_name"]),
                clean_value(row["event_url"]),
                clean_value(row["event_date"]),
                clean_value(row["event_time"]),
                clean_value(row["timezone"]),
                clean_value(row["event_status"]),
                clean_value(row["venue_id"]),
                clean_value(row["attraction_id"]),
                clean_value(row["segment"]),
                clean_value(row["genre"]),
                clean_value(row["subgenre"]),
                clean_value(row["promoter"]),
                clean_value(row["price_min"]),
                clean_value(row["price_max"]),
                clean_value(row["currency"]),
            )

            cursor.execute(
                """
                INSERT INTO events (
                    event_id,
                    event_name,
                    event_url,
                    event_date,
                    event_time,
                    timezone,
                    event_status,
                    venue_id,
                    attraction_id,
                    segment,
                    genre,
                    subgenre,
                    promoter,
                    price_min,
                    price_max,
                    currency
                )
                VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s
                )
                ON CONFLICT (event_id)
                DO UPDATE SET
                    event_name = EXCLUDED.event_name,
                    event_url = EXCLUDED.event_url,
                    event_date = EXCLUDED.event_date,
                    event_time = EXCLUDED.event_time,
                    timezone = EXCLUDED.timezone,
                    event_status = EXCLUDED.event_status,
                    venue_id = EXCLUDED.venue_id,
                    attraction_id = EXCLUDED.attraction_id,
                    segment = EXCLUDED.segment,
                    genre = EXCLUDED.genre,
                    subgenre = EXCLUDED.subgenre,
                    promoter = EXCLUDED.promoter,
                    price_min = EXCLUDED.price_min,
                    price_max = EXCLUDED.price_max,
                    currency = EXCLUDED.currency;
                """,
                values,
            )

    # HISTORICAL SNAPSHOT
    for _, row in df.iterrows():
        cursor.execute(
            """
            INSERT INTO event_snapshots (
                snapshot_date,
                event_id,
                event_name,
                event_date,
                event_time,
                timezone,
                event_status,
                venue_id,
                attraction_id,
                segment,
                genre,
                subgenre,
                promoter,
                price_min,
                price_max,
                currency
            )
            VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s
            )
            ON CONFLICT (snapshot_date, event_id)
            DO UPDATE SET
                event_name = EXCLUDED.event_name,
                event_date = EXCLUDED.event_date,
                event_time = EXCLUDED.event_time,
                timezone = EXCLUDED.timezone,
                event_status = EXCLUDED.event_status,
                venue_id = EXCLUDED.venue_id,
                attraction_id = EXCLUDED.attraction_id,
                segment = EXCLUDED.segment,
                genre = EXCLUDED.genre,
                subgenre = EXCLUDED.subgenre,
                promoter = EXCLUDED.promoter,
                price_min = EXCLUDED.price_min,
                price_max = EXCLUDED.price_max,
                currency = EXCLUDED.currency;
            """,
            (
                snapshot_date,
                clean_value(row["event_id"]),
                clean_value(row["event_name"]),
                clean_value(row["event_date"]),
                clean_value(row["event_time"]),
                clean_value(row["timezone"]),
                clean_value(row["event_status"]),
                clean_value(row["venue_id"]),
                clean_value(row["attraction_id"]),
                clean_value(row["segment"]),
                clean_value(row["genre"]),
                clean_value(row["subgenre"]),
                clean_value(row["promoter"]),
                clean_value(row["price_min"]),
                clean_value(row["price_max"]),
                clean_value(row["currency"]),
            ),
        )

    conn.commit()

    print(f"Snapshot date: {snapshot_date}")
    print(f"Processed {len(venues):,} venues.")
    print(f"Processed {len(attractions):,} attractions.")
    print(f"Processed {len(df):,} events.")
    print(f"Saved {len(df):,} historical event snapshots.")

    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()