import falcon
from models.connection import get_connection


class JenisPembayaranResource:

    # =========================
    # GET ALL
    # =========================
    def on_get(self, req, resp):

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
        SELECT
            id,
            kode,
            nama,

            akun_harta AS harta,
            akun_pendapatan AS pendapatan,
            akun_hutang AS hutang,

            tipe AS type,
            status

        FROM jenis_pembayaran
        ORDER BY id DESC
        """)

        data = cursor.fetchall()

        cursor.close()
        conn.close()

        resp.media = data
        resp.status = falcon.HTTP_200

    # =========================
    # CREATE
    # =========================
    def on_post(self, req, resp):

        body = req.media

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO jenis_pembayaran (

            nama,
            akun_harta,
            akun_pendapatan,
            akun_hutang,
            tipe,
            status

        )
        VALUES (%s, %s, %s, %s, %s, %s)
        """, (

            body.get("nama"),
            body.get("harta"),
            body.get("pendapatan"),
            body.get("hutang"),
            body.get("type", "Bebas"),
            body.get("status", "aktif")

        ))

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message": "Jenis pembayaran berhasil ditambahkan"
        }

        resp.status = falcon.HTTP_201


class JenisPembayaranByIdResource:

    # =========================
    # UPDATE
    # =========================
    def on_put(self, req, resp, id):

        body = req.media

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE jenis_pembayaran
        SET

            nama=%s,
            akun_harta=%s,
            akun_pendapatan=%s,
            akun_hutang=%s,
            tipe=%s,
            status=%s

        WHERE id=%s
        """, (

            body.get("nama"),
            body.get("harta"),
            body.get("pendapatan"),
            body.get("hutang"),
            body.get("type"),
            body.get("status"),
            id

        ))

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message": "Jenis pembayaran berhasil diupdate"
        }

        resp.status = falcon.HTTP_200

    # =========================
    # DELETE
    # =========================
    def on_delete(self, req, resp, id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        DELETE FROM jenis_pembayaran
        WHERE id=%s
        """, (id,))

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message": "Jenis pembayaran berhasil dihapus"
        }

        resp.status = falcon.HTTP_200