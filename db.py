import mysql.connector

def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="suman613212",
        database="bank_management_system"
    )

