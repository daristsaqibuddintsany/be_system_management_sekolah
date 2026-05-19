import mysql.connector


def get_connection(database=None):
    try:
        print("🔵 Mencoba koneksi MySQL...")

        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="test123",
            port=3306,
            database=database
        )

        print("🟢 Berhasil koneksi MySQL")
        return conn

    except mysql.connector.Error as e:
        print("❌ Gagal koneksi MySQL:", e)
        return None


def init_db():
    print("🔵 Mulai init database...")

    conn = None
    cursor = None

    try:
        # =========================
        # KONEK MYSQL
        # =========================
        conn = get_connection()

        if conn is None:
            print("❌ Koneksi gagal total")
            return

        cursor = conn.cursor()

        # =========================
        # BUAT DATABASE
        # =========================
        cursor.execute(
            "CREATE DATABASE IF NOT EXISTS db_sekolah"
        )

        print("🟢 Database siap")

        cursor.close()
        conn.close()

        # =========================
        # KONEK KE DATABASE
        # =========================
        conn = get_connection("db_sekolah")

        if conn is None:
            print("❌ Gagal koneksi ke db_sekolah")
            return

        cursor = conn.cursor()

        # =========================
        # TABLE USERS
        # =========================
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nama VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL
        )
        """)

        print("🟢 Table users siap")

        # =========================
        # TABLE SISWA
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

        print("🟢 Table siswa siap")

        conn.commit()

        print("🟢 SUCCESS: Database & tabel berhasil dibuat")

    except mysql.connector.Error as e:
        print("❌ ERROR MYSQL:", e)

    except Exception as e:
        print("❌ ERROR:", e)

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()

        print("🔵 Koneksi ditutup")


if __name__ == "__main__":
    init_db()