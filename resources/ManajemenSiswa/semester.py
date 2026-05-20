import falcon

from models.connection import get_connection


class SemesterResource:

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
        FROM semester
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
        INSERT INTO semester (

            tahun_ajaran,
            jenis_semester,
            nama_semester

        )
        VALUES (%s, %s, %s)
        """, (

            body.get("tahun_ajaran"),
            body.get("jenis_semester"),
            body.get("nama_semester")

        ))

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message":
            "Data semester berhasil ditambahkan"
        }

        resp.status = falcon.HTTP_201


class SemesterByIdResource:

    # =========================
    # UPDATE
    # =========================

    def on_put(self, req, resp, id):

        body = req.media

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE semester
        SET

            tahun_ajaran=%s,
            jenis_semester=%s,
            nama_semester=%s

        WHERE id=%s
        """, (

            body.get("tahun_ajaran"),
            body.get("jenis_semester"),
            body.get("nama_semester"),
            id

        ))

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message":
            "Data semester berhasil diupdate"
        }

        resp.status = falcon.HTTP_200

    # =========================
    # DELETE
    # =========================

    def on_delete(self, req, resp, id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        DELETE FROM semester
        WHERE id=%s
        """, (id,))

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message":
            "Data semester berhasil dihapus"
        }

        resp.status = falcon.HTTP_200