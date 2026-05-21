import falcon

from models.connection import get_connection


class JadwalMengajarResource:

    # =========================
    # GET ALL
    # =========================

    def on_get(self, req, resp):

        conn = None
        cursor = None

        try:

            tahun_ajaran = req.get_param(
                "tahun_ajaran"
            )

            conn = get_connection()

            cursor = conn.cursor(
                dictionary=True
            )

            # FILTER TAHUN AJARAN
            if tahun_ajaran:

                cursor.execute("""
                SELECT *
                FROM jadwal_mengajar
                WHERE tahun_ajaran=%s
                ORDER BY id DESC
                """, (tahun_ajaran,))

            else:

                cursor.execute("""
                SELECT *
                FROM jadwal_mengajar
                ORDER BY id DESC
                """)

            data = cursor.fetchall()

            # =========================
            # CONVERT TIME
            # =========================
            for item in data:

                if item.get("jam_mulai"):
                    item["jam_mulai"] = str(
                        item["jam_mulai"]
                    )

                if item.get("jam_selesai"):
                    item["jam_selesai"] = str(
                        item["jam_selesai"]
                    )

            resp.media = data

            resp.status = falcon.HTTP_200

        except Exception as e:

            print("ERROR GET:", str(e))

            resp.media = {
                "error": str(e)
            }

            resp.status = falcon.HTTP_500

        finally:

            if cursor:
                cursor.close()

            if conn:
                conn.close()

    # =========================
    # CREATE
    # =========================

    def on_post(self, req, resp):

        conn = None
        cursor = None

        try:

            body = req.media

            conn = get_connection()

            cursor = conn.cursor()

            cursor.execute("""
            INSERT INTO jadwal_mengajar (

                nama_guru,
                mata_pelajaran,
                kelas,
                hari,
                jam_mulai,
                jam_selesai,
                tahun_ajaran

            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (

                body.get("nama_guru"),
                body.get("mata_pelajaran"),
                body.get("kelas"),
                body.get("hari"),
                body.get("jam_mulai"),
                body.get("jam_selesai"),
                body.get("tahun_ajaran")

            ))

            conn.commit()

            resp.media = {
                "message":
                "Data jadwal mengajar berhasil ditambahkan"
            }

            resp.status = falcon.HTTP_201

        except Exception as e:

            print("ERROR POST:", str(e))

            resp.media = {
                "error": str(e)
            }

            resp.status = falcon.HTTP_500

        finally:

            if cursor:
                cursor.close()

            if conn:
                conn.close()


class JadwalMengajarByIdResource:

    # =========================
    # UPDATE
    # =========================

    def on_put(self, req, resp, id):

        conn = None
        cursor = None

        try:

            body = req.media

            conn = get_connection()

            cursor = conn.cursor()

            cursor.execute("""
            UPDATE jadwal_mengajar
            SET

                nama_guru=%s,
                mata_pelajaran=%s,
                kelas=%s,
                hari=%s,
                jam_mulai=%s,
                jam_selesai=%s,
                tahun_ajaran=%s

            WHERE id=%s
            """, (

                body.get("nama_guru"),
                body.get("mata_pelajaran"),
                body.get("kelas"),
                body.get("hari"),
                body.get("jam_mulai"),
                body.get("jam_selesai"),
                body.get("tahun_ajaran"),
                id

            ))

            conn.commit()

            resp.media = {
                "message":
                "Data jadwal mengajar berhasil diupdate"
            }

            resp.status = falcon.HTTP_200

        except Exception as e:

            print("ERROR PUT:", str(e))

            resp.media = {
                "error": str(e)
            }

            resp.status = falcon.HTTP_500

        finally:

            if cursor:
                cursor.close()

            if conn:
                conn.close()

    # =========================
    # DELETE
    # =========================

    def on_delete(self, req, resp, id):

        conn = None
        cursor = None

        try:

            conn = get_connection()

            cursor = conn.cursor()

            cursor.execute("""
            DELETE FROM jadwal_mengajar
            WHERE id=%s
            """, (id,))

            conn.commit()

            resp.media = {
                "message":
                "Data jadwal mengajar berhasil dihapus"
            }

            resp.status = falcon.HTTP_200

        except Exception as e:

            print("ERROR DELETE:", str(e))

            resp.media = {
                "error": str(e)
            }

            resp.status = falcon.HTTP_500

        finally:

            if cursor:
                cursor.close()

            if conn:
                conn.close()