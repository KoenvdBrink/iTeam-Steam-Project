import psycopg2
from numpy.ma.extras import average
from psycopg2 import sql

pguser = "postgres"
pgpass = "BrJaRePaBe2002"
database = "steamdatabase"
host = "172.167.28.110"
port = 5432


def fetch_average_playtime():
    try:
        # Gebruik mock-waarde
        print("[INFO] Gebruik van gecachede waarde omdat database niet draait.")
        # return 90.0  # Gemiddelde speeltijd in uren als voorbeeld voor testen
        # Establish connection
        conn = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=pguser,
            password=pgpass
        )
        playtime = 0
        games = 0

        # Create a cursor to interact with the database
        cursor = conn.cursor()

        # Execute a query
        cursor.execute("SELECT average_playtime_hrs FROM app_details;")

        # Fetch all rows from the executed query
        rows = cursor.fetchall()


        for row in rows:
            playtime += row[0]
            games += 1

    except psycopg2.Error as e:
        print(f"Error connecting to PostgreSQL database: {e}")

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()

        # pass voor testen
    return playtime/games
