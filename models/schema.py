import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="test123",
        database="db_sekolah",
        port=3306
    )


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # =========================
    # USERS
    # =========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nama VARCHAR(100) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL
    )
    """)

    # =========================
    # SISWA
    # =========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS siswa (
        id INT AUTO_INCREMENT PRIMARY KEY,

        nis VARCHAR(50) NOT NULL,
        nisn VARCHAR(50),

        nama VARCHAR(100) NOT NULL,

        tempat_lahir VARCHAR(100),
        tanggal_lahir DATE,

        jenis_kelamin VARCHAR(20),

        alamat TEXT,

        agama VARCHAR(50),
        golongan_darah VARCHAR(10),

        status VARCHAR(20),

        tahun_ajaran VARCHAR(20),
        tahun_masuk VARCHAR(20),

        kelas VARCHAR(50),
        jurusan VARCHAR(50),

        no_hp VARCHAR(20),

        sekolah_asal VARCHAR(100),

        ayah VARCHAR(100),
        pekerjaan_ayah VARCHAR(100),
        hp_ayah VARCHAR(20),

        ibu VARCHAR(100),
        pekerjaan_ibu VARCHAR(100),
        hp_ibu VARCHAR(20),

        wali VARCHAR(100),
        hp_wali VARCHAR(20),
        hubungan_wali VARCHAR(50)
    )
    """)

    conn.commit()

    cursor.close()
    conn.close()