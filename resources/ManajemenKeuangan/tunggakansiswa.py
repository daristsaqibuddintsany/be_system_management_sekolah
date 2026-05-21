import falcon
from models.connection import get_connection


class TunggakanSiswaResource:

    # =========================
    # GET ALL
    # =========================
    def on_get(self, req, resp):

        kelas = req.get_param("kelas")
        tahun = req.get_param("tahun")

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

            nominal AS totalTagihan,

            0 AS totalBayar,

            nominal AS tunggakan,

            CASE
                WHEN status='lunas'
                THEN 'Lunas'
                ELSE 'Belum Lunas'
            END AS status,

            keterangan

        FROM tunggakan_siswa

        WHERE 1=1
        """

        values = []

        # FILTER KELAS
        if kelas:
            query += " AND kelas=%s "
            values.append(kelas)

        # FILTER TAHUN
        if tahun:
            query += " AND tahun_ajaran=%s "
            values.append(tahun)

        query += """
        ORDER BY id DESC
        """

        cursor.execute(query, tuple(values))

        data = cursor.fetchall()

        cursor.close()
        conn.close()

        resp.media = {
            "data": data
        }

        resp.status = falcon.HTTP_200

    # =========================
    # CREATE
    # =========================
    def on_post(self, req, resp):

        body = req.media

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO tunggakan_siswa (

            siswa_id,
            nis,
            nama_siswa,
            kelas,
            tahun_ajaran,
            bulan,
            nominal,
            status,
            keterangan

        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (

            body.get("siswa_id"),
            body.get("nis"),
            body.get("nama_siswa"),
            body.get("kelas"),
            body.get("tahun_ajaran"),
            body.get("bulan"),
            body.get("nominal"),
            body.get("status", "belum_lunas"),
            body.get("keterangan")

        ))

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message": "Data tunggakan berhasil ditambahkan"
        }

        resp.status = falcon.HTTP_201


class TunggakanSiswaByIdResource:

    # =========================
    # UPDATE
    # =========================
    def on_put(self, req, resp, id):

        body = req.media

        conn = get_connection()
        cursor = conn.cursor()

        query = """
        UPDATE tunggakan_siswa
        SET
            status=%s
        """

        values = [
            body.get("status", "lunas").lower()
        ]

        # OPTIONAL UPDATE
        if body.get("keterangan") is not None:

            query += ", keterangan=%s "
            values.append(body.get("keterangan"))

        query += " WHERE id=%s "
        values.append(id)

        cursor.execute(query, tuple(values))

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message": "Status tunggakan berhasil diupdate"
        }

        resp.status = falcon.HTTP_200

    # =========================
    # DELETE
    # =========================
    def on_delete(self, req, resp, id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        DELETE FROM tunggakan_siswa
        WHERE id=%s
        """, (id,))

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message": "Data tunggakan berhasil dihapus"
        }

        resp.status = falcon.HTTP_200