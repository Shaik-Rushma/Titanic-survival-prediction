
import os
import pandas as pd
import psycopg2

def get_connection():
    password = os.getenv("DB_PASSWORD")

    if not password:
        raise RuntimeError("DB_PASSWORD is missing.")

    return psycopg2.connect(
        host="localhost",
        port="5432",
        database="titanic_db",
        user="postgres",
        password=password
    )

def run_query(query):
    conn = get_connection()
    try:
        df = pd.read_sql_query(query, conn)
        return df
    finally:
        conn.close()

