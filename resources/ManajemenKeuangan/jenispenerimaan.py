import falcon
from models.connection import get_connection


class JenisPenerimaanResource:

    # =========================
    # GET ALL
    # =========================
    def on_get(self, req, resp):

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
        SELECT *
        FROM jenis_penerimaan
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
        INSERT INTO jenis_penerimaan (

            akun_harta,
            kode_keuangan,
            kode,
            nama,
            jenis,
            keterangan,
            status

        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (

            body.get("akunHarta"),
            body.get("kodeKeuangan"),
            body.get("kode"),
            body.get("nama"),
            body.get("jenis"),
            body.get("keterangan"),
            body.get("status", "Aktif")

        ))

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message": "Jenis penerimaan berhasil ditambahkan"
        }

        resp.status = falcon.HTTP_201


class JenisPenerimaanByIdResource:

    # =========================
    # UPDATE
    # =========================
    def on_put(self, req, resp, id):

        body = req.media

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE jenis_penerimaan
        SET

            akun_harta=%s,
            kode_keuangan=%s,
            kode=%s,
            nama=%s,
            jenis=%s,
            keterangan=%s,
            status=%s

        WHERE id=%s
        """, (

            body.get("akunHarta"),
            body.get("kodeKeuangan"),
            body.get("kode"),
            body.get("nama"),
            body.get("jenis"),
            body.get("keterangan"),
            body.get("status"),
            id

        ))

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message": "Jenis penerimaan berhasil diupdate"
        }

        resp.status = falcon.HTTP_200

    # =========================
    # DELETE
    # =========================
    def on_delete(self, req, resp, id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        DELETE FROM jenis_penerimaan
        WHERE id=%s
        """, (id,))

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message": "Jenis penerimaan berhasil dihapus"
        }

        resp.status = falcon.HTTP_200