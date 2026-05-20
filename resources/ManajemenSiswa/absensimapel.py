import falcon

from models.connection import get_connection


class AbsensiMapelResource:

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
        FROM absensi_mapel
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
        INSERT INTO absensi_mapel (

            tanggal,
            jam_ke,
            mapel,
            guru,
            siswa,
            nis,
            status,
            keterangan,
            waktu

        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (

            body.get("tanggal"),
            body.get("jam_ke"),
            body.get("mapel"),
            body.get("guru"),
            body.get("siswa"),
            body.get("nis"),
            body.get("status"),
            body.get("keterangan"),
            body.get("waktu")

        ))

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message":
            "Absensi mapel berhasil ditambahkan"
        }

        resp.status = falcon.HTTP_201


class AbsensiMapelByIdResource:

    # =========================
    # UPDATE
    # =========================

    def on_put(self, req, resp, id):

        body = req.media

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE absensi_mapel
        SET

            tanggal=%s,
            jam_ke=%s,
            mapel=%s,
            guru=%s,
            siswa=%s,
            nis=%s,
            status=%s,
            keterangan=%s,
            waktu=%s

        WHERE id=%s
        """, (

            body.get("tanggal"),
            body.get("jam_ke"),
            body.get("mapel"),
            body.get("guru"),
            body.get("siswa"),
            body.get("nis"),
            body.get("status"),
            body.get("keterangan"),
            body.get("waktu"),
            id

        ))

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message":
            "Absensi mapel berhasil diupdate"
        }

        resp.status = falcon.HTTP_200

    # =========================
    # DELETE
    # =========================

    def on_delete(self, req, resp, id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        DELETE FROM absensi_mapel
        WHERE id=%s
        """, (id,))

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message":
            "Absensi mapel berhasil dihapus"
        }

        resp.status = falcon.HTTP_200