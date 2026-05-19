import falcon

from models.schema import get_connection


# ====================================
# DATA JURUSAN RESOURCE
# ====================================

class DataJurusanResource:

    # GET ALL
    def on_get(self, req, resp):

        try:

            conn = get_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute("""
                SELECT * FROM data_jurusan
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

            kode = media.get("kode")
            nama = media.get("nama")

            # VALIDASI
            if not kode or not nama:

                resp.status = falcon.HTTP_400

                resp.media = {
                    "status": False,
                    "message": "Kode dan Nama jurusan wajib diisi"
                }

                return

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO data_jurusan (
                    kode,
                    nama
                )
                VALUES (
                    %s,
                    %s
                )
            """, (
                kode,
                nama
            ))

            conn.commit()

            cursor.close()
            conn.close()

            resp.media = {
                "status": True,
                "message": "Data jurusan berhasil ditambahkan"
            }

        except Exception as e:

            resp.status = falcon.HTTP_500

            resp.media = {
                "status": False,
                "message": str(e)
            }


# ====================================
# DATA JURUSAN BY ID
# ====================================

class DataJurusanByIdResource:

    # GET BY ID
    def on_get(self, req, resp, id):

        try:

            conn = get_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute("""
                SELECT * FROM data_jurusan
                WHERE id=%s
            """, (id,))

            data = cursor.fetchone()

            cursor.close()
            conn.close()

            if not data:

                resp.status = falcon.HTTP_404

                resp.media = {
                    "status": False,
                    "message": "Data jurusan tidak ditemukan"
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

            kode = media.get("kode")
            nama = media.get("nama")

            if not kode or not nama:

                resp.status = falcon.HTTP_400

                resp.media = {
                    "status": False,
                    "message": "Kode dan Nama jurusan wajib diisi"
                }

                return

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE data_jurusan
                SET
                    kode=%s,
                    nama=%s
                WHERE id=%s
            """, (
                kode,
                nama,
                id
            ))

            conn.commit()

            cursor.close()
            conn.close()

            resp.media = {
                "status": True,
                "message": "Data jurusan berhasil diupdate"
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
                DELETE FROM data_jurusan
                WHERE id=%s
            """, (id,))

            conn.commit()

            cursor.close()
            conn.close()

            resp.media = {
                "status": True,
                "message": "Data jurusan berhasil dihapus"
            }

        except Exception as e:

            resp.status = falcon.HTTP_500

            resp.media = {
                "status": False,
                "message": str(e)
            }