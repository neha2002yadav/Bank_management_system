# db.py

import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Neha@123",
            database="bank_management_system"
        )
        if connection.is_connected():
            print("✅ Connected to MySQL database.")
            return connection
    except Error as e:
        print(f"❌ Database connection error: {e}")
        return None




