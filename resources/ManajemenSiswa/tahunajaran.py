import falcon

from models.connection import get_connection


class TahunAjaranResource:

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
        FROM tahun_ajaran
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

        tahun_ajaran = body.get(
            "tahun_ajaran"
        )

        tahun = body.get("tahun")

        status = body.get(
            "status",
            "Nonaktif"
        )

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO tahun_ajaran (

            tahun_ajaran,
            tahun,
            status

        )
        VALUES (%s, %s, %s)
        """, (

            tahun_ajaran,
            tahun,
            status

        ))

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message":
            "Tahun ajaran berhasil ditambahkan"
        }

        resp.status = falcon.HTTP_201


class TahunAjaranByIdResource:

    # =========================
    # UPDATE
    # =========================

    def on_put(self, req, resp, id):

        body = req.media

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE tahun_ajaran
        SET

            tahun_ajaran=%s,
            tahun=%s,
            status=%s

        WHERE id=%s
        """, (

            body.get("tahun_ajaran"),
            body.get("tahun"),
            body.get("status"),
            id

        ))

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message":
            "Tahun ajaran berhasil diupdate"
        }

        resp.status = falcon.HTTP_200

    # =========================
    # DELETE
    # =========================

    def on_delete(self, req, resp, id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        DELETE FROM tahun_ajaran
        WHERE id=%s
        """, (id,))

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message":
            "Tahun ajaran berhasil dihapus"
        }

        resp.status = falcon.HTTP_200