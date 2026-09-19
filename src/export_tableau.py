import os

import pandas as pd
import psycopg2
from dotenv import load_dotenv


load_dotenv()

OUTPUT_FILE = "data/event_snapshot_analysis.csv"

DB_CONFIG = {
    "host": "localhost",
    "database": "ticketmaster_analytics",
    "user": "postgres",
    "password": os.getenv("DB_PASSWORD"),
    "port": 5432,
}


def main():
    if not DB_CONFIG["password"]:
        raise ValueError("DB_PASSWORD is missing from .env")

    query = """
        SELECT *
        FROM event_snapshot_analysis
        ORDER BY snapshot_date, event_date, event_name;
    """

    conn = psycopg2.connect(**DB_CONFIG)

    try:
        df = pd.read_sql_query(query, conn)
    finally:
        conn.close()

    df.to_csv(OUTPUT_FILE, index=False)

    print(f"Exported {len(df):,} rows to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()