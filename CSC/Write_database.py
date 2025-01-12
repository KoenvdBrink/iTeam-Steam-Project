import pandas as pd
import psycopg2
from psycopg2 import sql

db_config = {
    'dbname': 'steamdatabase',
    'user': 'postgres',
    'password': 'BrJaRePaBe2002',
    'host': '172.167.28.110',  # Bijvoorbeeld 'localhost' of een serveradres
    'port': 5432          # Standaard PostgreSQL-poort
}

file_path = "D:\\School HU 2024-2025\\Steam Project\\app_details.csv"


def upload_csv_to_postgresql(file_path, db_config):
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        df = pd.read_csv(file_path)

        create_table_query = """
        CREATE TABLE IF NOT EXISTS app_details (
            AppID INTEGER PRIMARY KEY,
            Name TEXT,
            Average_Playtime_hrs FLOAT,
            Median_Playtime_hrs FLOAT,
            User_Score FLOAT,
            Peak_Players INTEGER
        )
        """
        cursor.execute(create_table_query)
        conn.commit()

        for _, row in df.iterrows():
            insert_query = sql.SQL(
                """
                INSERT INTO app_details (AppID, Name, Average_Playtime_hrs, Median_Playtime_hrs, User_Score, Peak_Players)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (AppID) DO NOTHING
                """
            )
            cursor.execute(insert_query, (
                row['AppID'], row['Name'], row['Average Playtime (hrs)'],
                row['Median Playtime (hrs)'], row['User Score (%)'], row['Peak Players']
            ))


        conn.commit()
        cursor.close()
        conn.close()

        print("Data succesvol geüpload naar de database!")

    except Exception as e:
        print(f"Fout bij het uploaden van data: {e}")

upload_csv_to_postgresql(file_path, db_config)
