import falcon

from models.connection import get_connection


class JenisSemesterResource:

    # =========================
    # GET ALL
    # =========================

    def on_get(self, req, resp):

        conn = get_connection()

        cursor = conn.cursor(
            dictionary=True
        )

        cursor.execute("""
        SELECT *
        FROM jenis_semester
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

        nama = body.get("nama")

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO jenis_semester (
            nama
        )
        VALUES (%s)
        """, (nama,))

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message":
            "Jenis semester berhasil ditambahkan"
        }

        resp.status = falcon.HTTP_201


class JenisSemesterByIdResource:

    # =========================
    # UPDATE
    # =========================

    def on_put(self, req, resp, id):

        body = req.media

        nama = body.get("nama")

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE jenis_semester
        SET nama=%s
        WHERE id=%s
        """, (
            nama,
            id
        ))

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message":
            "Jenis semester berhasil diupdate"
        }

        resp.status = falcon.HTTP_200

    # =========================
    # DELETE
    # =========================

    def on_delete(self, req, resp, id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        DELETE FROM jenis_semester
        WHERE id=%s
        """, (id,))

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message":
            "Jenis semester berhasil dihapus"
        }

        resp.status = falcon.HTTP_200