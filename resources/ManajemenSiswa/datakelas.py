import falcon

from models.schema import get_connection


# ====================================
# DATA KELAS RESOURCE
# ====================================

class DataKelasResource:

    # GET ALL
    def on_get(self, req, resp):

        try:

            conn = get_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute("""
                SELECT * FROM data_kelas
                ORDER BY id DESC
            """)

            data = cursor.fetchall()

            cursor.close()
            conn.close()

            resp.media = data

        except Exception as e:

            resp.status = falcon.HTTP_500
            resp.media = {
                "status": False,
                "message": str(e)
            }

    # CREATE
    def on_post(self, req, resp):

        try:

            media = req.media

            kelas = media.get("kelas")
            jurusan = media.get("jurusan")

            # VALIDASI
            if not kelas or not jurusan:

                resp.status = falcon.HTTP_400

                resp.media = {
                    "status": False,
                    "message": "Kelas dan Jurusan wajib diisi"
                }

                return

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO data_kelas (
                    kelas,
                    jurusan
                )
                VALUES (
                    %s,
                    %s
                )
            """, (
                kelas,
                jurusan
            ))

            conn.commit()

            cursor.close()
            conn.close()

            resp.media = {
                "status": True,
                "message": "Data kelas berhasil ditambahkan"
            }

        except Exception as e:

            resp.status = falcon.HTTP_500

            resp.media = {
                "status": False,
                "message": str(e)
            }


# ====================================
# DATA KELAS BY ID
# ====================================

class DataKelasByIdResource:

    # GET BY ID
    def on_get(self, req, resp, id):

        try:

            conn = get_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute("""
                SELECT * FROM data_kelas
                WHERE id=%s
            """, (id,))

            data = cursor.fetchone()

            cursor.close()
            conn.close()

            if not data:

                resp.status = falcon.HTTP_404

                resp.media = {
                    "status": False,
                    "message": "Data kelas tidak ditemukan"
                }

                return

            resp.media = data

        except Exception as e:

            resp.status = falcon.HTTP_500

            resp.media = {
                "status": False,
                "message": str(e)
            }

    # UPDATE
    def on_put(self, req, resp, id):

        try:

            media = req.media

            kelas = media.get("kelas")
            jurusan = media.get("jurusan")

            if not kelas or not jurusan:

                resp.status = falcon.HTTP_400

                resp.media = {
                    "status": False,
                    "message": "Kelas dan Jurusan wajib diisi"
                }

                return

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE data_kelas
                SET
                    kelas=%s,
                    jurusan=%s
                WHERE id=%s
            """, (
                kelas,
                jurusan,
                id
            ))

            conn.commit()

            cursor.close()
            conn.close()

            resp.media = {
                "status": True,
                "message": "Data kelas berhasil diupdate"
            }

        except Exception as e:

            resp.status = falcon.HTTP_500

            resp.media = {
                "status": False,
                "message": str(e)
            }

    # DELETE
    def on_delete(self, req, resp, id):

        try:

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                DELETE FROM data_kelas
                WHERE id=%s
            """, (id,))

            conn.commit()

            cursor.close()
            conn.close()

            resp.media = {
                "status": True,
                "message": "Data kelas berhasil dihapus"
            }

        except Exception as e:

            resp.status = falcon.HTTP_500

            resp.media = {
                "status": False,
                "message": str(e)
            }