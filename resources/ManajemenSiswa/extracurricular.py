import falcon

from models.schema import get_connection


# ====================================
# EXTRACURRICULAR RESOURCE
# ====================================

class ExtracurricularResource:

    # GET ALL
    def on_get(self, req, resp):

        try:

            conn = get_connection()

            cursor = conn.cursor(dictionary=True)

            cursor.execute("""
                SELECT * FROM extracurricular
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

            nama = media.get("nama")
            pembina = media.get("pembina")
            jadwal = media.get("jadwal")
            keterangan = media.get("keterangan")

            # VALIDASI
            if not nama:

                resp.status = falcon.HTTP_400

                resp.media = {
                    "status": False,
                    "message": "Nama extracurricular wajib diisi"
                }

                return

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO extracurricular (

                    nama,
                    pembina,
                    jadwal,
                    keterangan

                )
                VALUES (

                    %s,
                    %s,
                    %s,
                    %s

                )
            """, (
                nama,
                pembina,
                jadwal,
                keterangan
            ))

            conn.commit()

            cursor.close()
            conn.close()

            resp.media = {
                "status": True,
                "message": "Data extracurricular berhasil ditambahkan"
            }

        except Exception as e:

            resp.status = falcon.HTTP_500

            resp.media = {
                "status": False,
                "message": str(e)
            }


# ====================================
# EXTRACURRICULAR BY ID
# ====================================

class ExtracurricularByIdResource:

    # GET BY ID
    def on_get(self, req, resp, id):

        try:

            conn = get_connection()

            cursor = conn.cursor(dictionary=True)

            cursor.execute("""
                SELECT * FROM extracurricular
                WHERE id=%s
            """, (id,))

            data = cursor.fetchone()

            cursor.close()
            conn.close()

            if not data:

                resp.status = falcon.HTTP_404

                resp.media = {
                    "status": False,
                    "message": "Data extracurricular tidak ditemukan"
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

            nama = media.get("nama")
            pembina = media.get("pembina")
            jadwal = media.get("jadwal")
            keterangan = media.get("keterangan")

            if not nama:

                resp.status = falcon.HTTP_400

                resp.media = {
                    "status": False,
                    "message": "Nama extracurricular wajib diisi"
                }

                return

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE extracurricular
                SET

                    nama=%s,
                    pembina=%s,
                    jadwal=%s,
                    keterangan=%s

                WHERE id=%s
            """, (
                nama,
                pembina,
                jadwal,
                keterangan,
                id
            ))

            conn.commit()

            cursor.close()
            conn.close()

            resp.media = {
                "status": True,
                "message": "Data extracurricular berhasil diupdate"
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
                DELETE FROM extracurricular
                WHERE id=%s
            """, (id,))

            conn.commit()

            cursor.close()
            conn.close()

            resp.media = {
                "status": True,
                "message": "Data extracurricular berhasil dihapus"
            }

        except Exception as e:

            resp.status = falcon.HTTP_500

            resp.media = {
                "status": False,
                "message": str(e)
            }