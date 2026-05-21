import falcon
from models.connection import get_connection


class BayarTagihanResource:

    # =========================
    # GET LIST PEMBAYARAN
    # =========================
    def on_get(self, req, resp):

        tahun = req.get_param("tahun_ajaran")
        search = req.get_param("search")

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT
            id,
            siswa_id,
            nis,
            nama_siswa AS nama,
            kelas,
            tahun_ajaran,
            bulan,
            jumlah_bayar,
            status,
            tanggal_bayar
        FROM pembayaran
        WHERE 1=1
        """

        params = []

        # FILTER TAHUN AJARAN
        if tahun:
            query += " AND tahun_ajaran = %s"
            params.append(tahun)

        # FILTER SEARCH
        if search:
            query += """
            AND (
                nis LIKE %s
                OR nama_siswa LIKE %s
            )
            """
            params.append(f"%{search}%")
            params.append(f"%{search}%")

        query += " ORDER BY id DESC"

        cursor.execute(query, params)

        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        resp.media = rows
        resp.status = falcon.HTTP_200


class BayarTagihanCreateResource:

    # =========================
    # CREATE PEMBAYARAN
    # =========================
    def on_post(self, req, resp):

        body = req.media

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO pembayaran (
            siswa_id,
            nis,
            nama_siswa,
            kelas,
            jenis_pembayaran_id,
            bulan,
            tahun_ajaran,
            jumlah_bayar,
            status,
            tanggal_bayar
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            body["siswa_id"],
            body["nis"],
            body["nama_siswa"],
            body["kelas"],
            body["jenis_pembayaran_id"],
            body["bulan"],
            body["tahun_ajaran"],
            body["jumlah_bayar"],
            body.get("status", "lunas"),
            body.get("tanggal_bayar")
        ))

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message": "Pembayaran berhasil disimpan"
        }

        resp.status = falcon.HTTP_201


class BayarTagihanByIdResource:

    # =========================
    # DELETE PEMBAYARAN
    # =========================
    def on_delete(self, req, resp, id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        DELETE FROM pembayaran
        WHERE id = %s
        """, (id,))

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message": "Data pembayaran berhasil dihapus"
        }

        resp.status = falcon.HTTP_200