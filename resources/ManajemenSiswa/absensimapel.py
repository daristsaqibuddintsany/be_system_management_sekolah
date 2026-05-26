import falcon
import traceback

from datetime import date, datetime, time, timedelta

from models.connection import get_connection


class AbsensiMapelResource:

    # =========================
    # GET ALL
    # =========================
    def on_get(self, req, resp):

        conn = None
        cursor = None

        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute("""
                SELECT
                    id,
                    tanggal,
                    jam_ke,
                    mapel,
                    guru,
                    siswa,
                    nis,
                    status,
                    keterangan,
                    waktu
                FROM absensi_mapel
                ORDER BY id DESC
            """)

            rows = cursor.fetchall()

            result = []

            for row in rows:
                item = {}

                for key, value in row.items():

                    # =========================
                    # TANGGAL
                    # =========================
                    if key == "tanggal" and value:
                        try:
                            item[key] = value.strftime("%Y-%m-%d")
                        except:
                            item[key] = str(value)

                    # =========================
                    # WAKTU (FIX TOTAL SIMPLE)
                    # =========================
                    elif key == "waktu" and value:
                        item[key] = str(value)[:5]  # HH:MM aman

                    # =========================
                    # DATETIME
                    # =========================
                    elif isinstance(value, (datetime, date)):
                        item[key] = value.strftime("%Y-%m-%d")

                    elif value is None:
                        item[key] = ""

                    else:
                        item[key] = value

                result.append(item)

            resp.media = result
            resp.status = falcon.HTTP_200

        except Exception as e:
            traceback.print_exc()
            resp.media = {"success": False, "error": str(e)}
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
            body = req.media or {}

            conn = get_connection()
            cursor = conn.cursor()

            # =========================
            # FIX TANGGAL FLEXIBLE
            # =========================
            tanggal = body.get("tanggal")

            if tanggal:
                try:
                    if "-" in tanggal:
                        tanggal = datetime.strptime(tanggal, "%Y-%m-%d")
                    else:
                        tanggal = datetime.strptime(tanggal, "%d/%m/%Y")
                    tanggal = tanggal.strftime("%Y-%m-%d")
                except:
                    pass

            # =========================
            # WAKTU FIX
            # =========================
            waktu = body.get("waktu")
            if waktu:
                waktu = waktu.replace(".", ":")[:5]

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
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, (
                tanggal,
                body.get("jam_ke"),
                body.get("mapel"),
                body.get("guru"),
                body.get("siswa"),
                body.get("nis"),
                body.get("status"),
                body.get("keterangan"),
                waktu
            ))

            conn.commit()

            resp.media = {
                "success": True,
                "message": "Absensi berhasil ditambahkan"
            }
            resp.status = falcon.HTTP_201

        except Exception as e:
            traceback.print_exc()
            if conn:
                conn.rollback()

            resp.media = {"success": False, "error": str(e)}
            resp.status = falcon.HTTP_500

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()


class AbsensiMapelByIdResource:

    # =========================
    # UPDATE
    # =========================
    def on_put(self, req, resp, id):

        conn = None
        cursor = None

        try:
            body = req.media or {}

            conn = get_connection()
            cursor = conn.cursor()

            # =========================
            # TANGGAL FIX
            # =========================
            tanggal = body.get("tanggal")

            if tanggal:
                try:
                    if "-" in tanggal:
                        tanggal = datetime.strptime(tanggal, "%Y-%m-%d")
                    else:
                        tanggal = datetime.strptime(tanggal, "%d/%m/%Y")
                    tanggal = tanggal.strftime("%Y-%m-%d")
                except:
                    pass

            # =========================
            # WAKTU FIX
            # =========================
            waktu = body.get("waktu")
            if waktu:
                waktu = waktu.replace(".", ":")[:5]

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
                tanggal,
                body.get("jam_ke"),
                body.get("mapel"),
                body.get("guru"),
                body.get("siswa"),
                body.get("nis"),
                body.get("status"),
                body.get("keterangan"),
                waktu,
                id
            ))

            conn.commit()

            resp.media = {
                "success": True,
                "message": "Berhasil update"
            }
            resp.status = falcon.HTTP_200

        except Exception as e:
            traceback.print_exc()
            if conn:
                conn.rollback()

            resp.media = {"success": False, "error": str(e)}
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
                DELETE FROM absensi_mapel
                WHERE id=%s
            """, (id,))

            conn.commit()

            resp.media = {
                "success": True,
                "message": "Berhasil hapus"
            }
            resp.status = falcon.HTTP_200

        except Exception as e:
            traceback.print_exc()

            if conn:
                conn.rollback()

            resp.media = {"success": False, "error": str(e)}
            resp.status = falcon.HTTP_500

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()