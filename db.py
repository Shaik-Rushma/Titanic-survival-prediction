
import pandas as pd
import psycopg2

DB_CONFIG = {
    "host": "localhost",
    "port": "5432",
    "database": "titanic_db",
    "user": "postgres",
    "password": "Password"
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def run_query(query):
    conn = get_connection()

    try:
        df = pd.read_sql_query(query, conn)
        return df
    finally:
        conn.close()
