import falcon
from models.connection import get_connection


class SettingGPSResource:

    # =========================
    # GET ALL GPS
    # =========================
    def on_get(self, req, resp):

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
        SELECT *
        FROM setting_gps
        ORDER BY id DESC
        """)

        data = cursor.fetchall()

        cursor.close()
        conn.close()

        resp.media = data

    # =========================
    # CREATE GPS
    # =========================
    def on_post(self, req, resp):

        data = req.media

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO setting_gps (
            nama,
            latitude,
            longitude,
            radius,
            jam_masuk,
            jam_selesai
        ) VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            data["nama"],
            data["lat"],
            data["long"],
            data["radius"],
            data["masuk"],
            data["selesai"]
        ))

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message": "Lokasi GPS berhasil ditambahkan"
        }


class SettingGPSByIdResource:

    # =========================
    # GET BY ID
    # =========================
    def on_get(self, req, resp, id):

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
        SELECT *
        FROM setting_gps
        WHERE id = %s
        """, (id,))

        data = cursor.fetchone()

        cursor.close()
        conn.close()

        if not data:
            resp.status = falcon.HTTP_404
            resp.media = {"message": "Data tidak ditemukan"}
            return

        resp.media = data

    # =========================
    # UPDATE BY ID
    # =========================
    def on_put(self, req, resp, id):

        data = req.media

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE setting_gps
        SET
            nama = %s,
            latitude = %s,
            longitude = %s,
            radius = %s,
            jam_masuk = %s,
            jam_selesai = %s
        WHERE id = %s
        """, (
            data["nama"],
            data["lat"],
            data["long"],
            data["radius"],
            data["masuk"],
            data["selesai"],
            id
        ))

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message": "Lokasi GPS berhasil diupdate"
        }

    # =========================
    # DELETE BY ID
    # =========================
    def on_delete(self, req, resp, id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        DELETE FROM setting_gps
        WHERE id = %s
        """, (id,))

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message": "Lokasi GPS berhasil dihapus"
        }