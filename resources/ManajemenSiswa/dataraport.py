import falcon

from models.connection import get_connection


class DataRaportResource:

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
        FROM data_raport
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
        INSERT INTO data_raport (

            kelas,
            tahun_ajaran,
            semester,
            wali_kelas,
            mata_pelajaran

        )
        VALUES (%s, %s, %s, %s, %s)
        """, (

            body.get("kelas"),
            body.get("tahun_ajaran"),
            body.get("semester"),
            body.get("wali_kelas"),
            body.get("mata_pelajaran")

        ))

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message":
            "Data raport berhasil ditambahkan"
        }

        resp.status = falcon.HTTP_201


class DataRaportByIdResource:

    # =========================
    # UPDATE
    # =========================

    def on_put(self, req, resp, id):

        body = req.media

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE data_raport
        SET

            kelas=%s,
            tahun_ajaran=%s,
            semester=%s,
            wali_kelas=%s,
            mata_pelajaran=%s

        WHERE id=%s
        """, (

            body.get("kelas"),
            body.get("tahun_ajaran"),
            body.get("semester"),
            body.get("wali_kelas"),
            body.get("mata_pelajaran"),
            id

        ))

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message":
            "Data raport berhasil diupdate"
        }

        resp.status = falcon.HTTP_200

    # =========================
    # DELETE
    # =========================

    def on_delete(self, req, resp, id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        DELETE FROM data_raport
        WHERE id=%s
        """, (id,))

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message":
            "Data raport berhasil dihapus"
        }

        resp.status = falcon.HTTP_200