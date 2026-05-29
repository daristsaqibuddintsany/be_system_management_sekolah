import falcon
import os
import time

from models.connection import get_connection


class BannerAplikasiResource:

    # =========================
    # GET ALL BANNER
    # =========================
    def on_get(self, req, resp):

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
        SELECT *
        FROM banner_aplikasi
        ORDER BY id DESC
        """)

        data = cursor.fetchall()

        cursor.close()
        conn.close()

        resp.media = data

    # =========================
    # UPLOAD BANNER
    # =========================
    def on_post(self, req, resp):

        file = req.get_param("file")

        if not file:
            resp.status = falcon.HTTP_400
            resp.media = {"message": "File tidak ditemukan"}
            return

        upload_dir = "uploads/banner"

        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

        filename = f"banner_{int(time.time())}.jpg"
        file_path = os.path.join(upload_dir, filename)

        # simpan file
        with open(file_path, "wb") as f:
            f.write(file.file.read())

        conn = get_connection()
        cursor = conn.cursor()

        preview_url = f"/uploads/banner/{filename}"

        cursor.execute("""
        INSERT INTO banner_aplikasi (
            nama_file,
            path_file,
            preview_url
        ) VALUES (%s, %s, %s)
        """, (
            filename,
            file_path,
            preview_url
        ))

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message": "Banner berhasil diupload",
            "filename": filename,
            "preview": preview_url
        }


class BannerAplikasiByIdResource:

    # =========================
    # DELETE BANNER
    # =========================
    def on_delete(self, req, resp, id):

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
        SELECT *
        FROM banner_aplikasi
        WHERE id = %s
        """, (id,))

        data = cursor.fetchone()

        if not data:
            resp.status = falcon.HTTP_404
            resp.media = {"message": "Data tidak ditemukan"}
            return

        # hapus file fisik
        if os.path.exists(data["path_file"]):
            os.remove(data["path_file"])

        cursor.execute("""
        DELETE FROM banner_aplikasi
        WHERE id = %s
        """, (id,))

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message": "Banner berhasil dihapus"
        }