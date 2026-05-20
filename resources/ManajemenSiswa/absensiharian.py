import falcon

from models.connection import get_connection


class AbsensiHarianResource:

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
        FROM absensi_harian
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
        INSERT INTO absensi_harian (

            tanggal,
            nis,
            nama,
            kelas,
            jam_masuk,
            status_masuk,
            jam_pulang,
            status_pulang,
            keterangan

        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (

            body.get("tanggal"),
            body.get("nis"),
            body.get("nama"),
            body.get("kelas"),
            body.get("jam_masuk"),
            body.get("status_masuk"),
            body.get("jam_pulang"),
            body.get("status_pulang"),
            body.get("keterangan")

        ))

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message":
            "Data absensi berhasil ditambahkan"
        }

        resp.status = falcon.HTTP_201


class AbsensiHarianByIdResource:

    # =========================
    # UPDATE
    # =========================

    def on_put(self, req, resp, id):

        body = req.media

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE absensi_harian
        SET

            tanggal=%s,
            nis=%s,
            nama=%s,
            kelas=%s,
            jam_masuk=%s,
            status_masuk=%s,
            jam_pulang=%s,
            status_pulang=%s,
            keterangan=%s

        WHERE id=%s
        """, (

            body.get("tanggal"),
            body.get("nis"),
            body.get("nama"),
            body.get("kelas"),
            body.get("jam_masuk"),
            body.get("status_masuk"),
            body.get("jam_pulang"),
            body.get("status_pulang"),
            body.get("keterangan"),
            id

        ))

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message":
            "Data absensi berhasil diupdate"
        }

        resp.status = falcon.HTTP_200

    # =========================
    # DELETE
    # =========================

    def on_delete(self, req, resp, id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        DELETE FROM absensi_harian
        WHERE id=%s
        """, (id,))

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message":
            "Data absensi berhasil dihapus"
        }

        resp.status = falcon.HTTP_200