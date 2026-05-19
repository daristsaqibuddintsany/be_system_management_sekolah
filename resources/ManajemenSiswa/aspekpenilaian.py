import falcon

from models.schema import get_connection


# ====================================
# ASPEK PENILAIAN RESOURCE
# ====================================

class AspekPenilaianResource:

    # GET ALL
    def on_get(self, req, resp):

        try:

            conn = get_connection()

            cursor = conn.cursor(dictionary=True)

            cursor.execute("""
                SELECT * FROM aspek_penilaian
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
            keterangan = media.get("keterangan")
            editable = media.get("editable", True)

            # VALIDASI
            if not nama:

                resp.status = falcon.HTTP_400

                resp.media = {
                    "status": False,
                    "message": "Nama aspek wajib diisi"
                }

                return

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO aspek_penilaian (

                    nama,
                    keterangan,
                    editable

                )
                VALUES (

                    %s,
                    %s,
                    %s

                )
            """, (
                nama,
                keterangan,
                editable
            ))

            conn.commit()

            cursor.close()
            conn.close()

            resp.media = {
                "status": True,
                "message": "Aspek penilaian berhasil ditambahkan"
            }

        except Exception as e:

            resp.status = falcon.HTTP_500

            resp.media = {
                "status": False,
                "message": str(e)
            }


# ====================================
# ASPEK PENILAIAN BY ID
# ====================================

class AspekPenilaianByIdResource:

    # GET BY ID
    def on_get(self, req, resp, id):

        try:

            conn = get_connection()

            cursor = conn.cursor(dictionary=True)

            cursor.execute("""
                SELECT * FROM aspek_penilaian
                WHERE id=%s
            """, (id,))

            data = cursor.fetchone()

            cursor.close()
            conn.close()

            if not data:

                resp.status = falcon.HTTP_404

                resp.media = {
                    "status": False,
                    "message": "Aspek penilaian tidak ditemukan"
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
            keterangan = media.get("keterangan")
            editable = media.get("editable", True)

            if not nama:

                resp.status = falcon.HTTP_400

                resp.media = {
                    "status": False,
                    "message": "Nama aspek wajib diisi"
                }

                return

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE aspek_penilaian
                SET

                    nama=%s,
                    keterangan=%s,
                    editable=%s

                WHERE id=%s
            """, (
                nama,
                keterangan,
                editable,
                id
            ))

            conn.commit()

            cursor.close()
            conn.close()

            resp.media = {
                "status": True,
                "message": "Aspek penilaian berhasil diupdate"
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

            cursor = conn.cursor(dictionary=True)

            # CEK LOCK
            cursor.execute("""
                SELECT editable
                FROM aspek_penilaian
                WHERE id=%s
            """, (id,))

            data = cursor.fetchone()

            if not data:

                resp.status = falcon.HTTP_404

                resp.media = {
                    "status": False,
                    "message": "Data tidak ditemukan"
                }

                return

            # LOCKED SYSTEM
            if not data["editable"]:

                resp.status = falcon.HTTP_403

                resp.media = {
                    "status": False,
                    "message": "Aspek sistem tidak bisa dihapus"
                }

                return

            cursor.execute("""
                DELETE FROM aspek_penilaian
                WHERE id=%s
            """, (id,))

            conn.commit()

            cursor.close()
            conn.close()

            resp.media = {
                "status": True,
                "message": "Aspek penilaian berhasil dihapus"
            }

        except Exception as e:

            resp.status = falcon.HTTP_500

            resp.media = {
                "status": False,
                "message": str(e)
            }