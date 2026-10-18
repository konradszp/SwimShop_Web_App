import mysql.connector
from mysql.connector import Error
from backend.config import DB_CONFIG

def get_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None