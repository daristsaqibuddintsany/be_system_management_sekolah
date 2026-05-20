import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="test123",
        database="db_sekolah",
        port=3306
    )