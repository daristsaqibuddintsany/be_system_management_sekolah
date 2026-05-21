import falcon

from models.connection import get_connection


class MataPelajaranResource:

    # =========================
    # GET ALL
    # =========================

    def on_get(self, req, resp):

        search = req.get_param("search")

        conn = get_connection()

        cursor = conn.cursor(
            dictionary=True
        )

        # SEARCH
        if search:

            cursor.execute("""
            SELECT *
            FROM mata_pelajaran
            WHERE nama LIKE %s
            ORDER BY id DESC
            """, (f"%{search}%",))

        else:

            cursor.execute("""
            SELECT *
            FROM mata_pelajaran
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
        INSERT INTO mata_pelajaran (

            nama

        )
        VALUES (%s)
        """, (

            body.get("nama"),

        ))

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message":
            "Mata pelajaran berhasil ditambahkan"
        }

        resp.status = falcon.HTTP_201


class MataPelajaranByIdResource:

    # =========================
    # UPDATE
    # =========================

    def on_put(self, req, resp, id):

        body = req.media

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
        UPDATE mata_pelajaran
        SET

            nama=%s

        WHERE id=%s
        """, (

            body.get("nama"),
            id

        ))

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message":
            "Mata pelajaran berhasil diupdate"
        }

        resp.status = falcon.HTTP_200

    # =========================
    # DELETE
    # =========================

    def on_delete(self, req, resp, id):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
        DELETE FROM mata_pelajaran
        WHERE id=%s
        """, (id,))

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message":
            "Mata pelajaran berhasil dihapus"
        }

        resp.status = falcon.HTTP_200