import falcon

from models.connection import get_connection


class WaliKelasResource:

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
        FROM wali_kelas
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
        INSERT INTO wali_kelas (

            nama_kelas,
            nama_pegawai,
            tahun_ajaran

        )
        VALUES (%s, %s, %s)
        """, (

            body.get("nama_kelas"),
            body.get("nama_pegawai"),
            body.get("tahun_ajaran")

        ))

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message":
            "Data wali kelas berhasil ditambahkan"
        }

        resp.status = falcon.HTTP_201


class WaliKelasByIdResource:

    # =========================
    # UPDATE
    # =========================

    def on_put(self, req, resp, id):

        body = req.media

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE wali_kelas
        SET

            nama_kelas=%s,
            nama_pegawai=%s,
            tahun_ajaran=%s

        WHERE id=%s
        """, (

            body.get("nama_kelas"),
            body.get("nama_pegawai"),
            body.get("tahun_ajaran"),
            id

        ))

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message":
            "Data wali kelas berhasil diupdate"
        }

        resp.status = falcon.HTTP_200

    # =========================
    # DELETE
    # =========================

    def on_delete(self, req, resp, id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        DELETE FROM wali_kelas
        WHERE id=%s
        """, (id,))

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message":
            "Data wali kelas berhasil dihapus"
        }

        resp.status = falcon.HTTP_200