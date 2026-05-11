import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="test123",
    database="db_sekolah"
)

print("KONEKSI BERHASIL")