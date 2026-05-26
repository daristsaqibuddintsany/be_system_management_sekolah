import falcon
from models.connection import get_connection


# =====================================================
# AUTO CREATE TABLE
# =====================================================

def create_realisasi_belanja_table(cursor):

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS realisasi_belanja (
        id INT AUTO_INCREMENT PRIMARY KEY,

        kode_akun VARCHAR(30) NOT NULL,
        nama_akun VARCHAR(100) NOT NULL,

        bulan VARCHAR(20) NOT NULL,

        tahun_ajaran VARCHAR(20) NOT NULL,

        nominal BIGINT NOT NULL DEFAULT 0,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ON UPDATE CURRENT_TIMESTAMP

    ) ENGINE=InnoDB
    """)


class RealisasiBelanjaResource:

    # =====================================================
    # GET LAPORAN
    # =====================================================

    def on_get(self, req, resp):

        tahun = req.get_param("tahun")

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # AUTO CREATE TABLE
        create_realisasi_belanja_table(cursor)

        query = """
        SELECT
            kode_akun,
            nama_akun,
            bulan,
            SUM(nominal) AS total
        FROM realisasi_belanja
        WHERE 1=1
        """

        values = []

        # FILTER TAHUN AJARAN
        if tahun:
            query += " AND tahun_ajaran=%s "
            values.append(tahun)

        query += """
        GROUP BY
            kode_akun,
            nama_akun,
            bulan

        ORDER BY
            kode_akun ASC
        """

        cursor.execute(query, tuple(values))

        raw_data = cursor.fetchall()

        bulan_urutan = [
            "Juli",
            "Agustus",
            "September",
            "Oktober",
            "November",
            "Desember",
            "Januari",
            "Februari",
            "Maret",
            "April",
            "Mei",
            "Juni"
        ]

        hasil = {}

        # FORMAT DATA
        for row in raw_data:

            kode = row["kode_akun"]

            if kode not in hasil:

                hasil[kode] = {
                    "kode": row["kode_akun"],
                    "nama": row["nama_akun"],
                    "bulan": [0] * 12
                }

            bulan_index = bulan_urutan.index(row["bulan"])

            hasil[kode]["bulan"][bulan_index] = int(row["total"])

        data = list(hasil.values())

        cursor.close()
        conn.close()

        resp.media = {
            "data": data
        }

        resp.status = falcon.HTTP_200

    # =====================================================
    # CREATE DATA
    # =====================================================

    def on_post(self, req, resp):

        body = req.media

        conn = get_connection()
        cursor = conn.cursor()

        # AUTO CREATE TABLE
        create_realisasi_belanja_table(cursor)

        cursor.execute("""
        INSERT INTO realisasi_belanja (

            kode_akun,
            nama_akun,
            bulan,
            tahun_ajaran,
            nominal

        )
        VALUES (%s, %s, %s, %s, %s)
        """, (

            body.get("kode_akun"),
            body.get("nama_akun"),
            body.get("bulan"),
            body.get("tahun_ajaran"),
            body.get("nominal", 0)

        ))

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message": "Data realisasi belanja berhasil ditambahkan"
        }

        resp.status = falcon.HTTP_201


class RealisasiBelanjaByIdResource:

    # =====================================================
    # DELETE
    # =====================================================

    def on_delete(self, req, resp, id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        DELETE FROM realisasi_belanja
        WHERE id=%s
        """, (id,))

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message": "Data realisasi belanja berhasil dihapus"
        }

        resp.status = falcon.HTTP_200