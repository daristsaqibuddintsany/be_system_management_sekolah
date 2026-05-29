
import falcon
import traceback

from models.connection import get_connection


class BayarTagihanResource:

    # =========================
    # GET LIST PEMBAYARAN
    # =========================

    def on_get(self, req, resp):

        conn = None
        cursor = None

        try:

            tahun = req.get_param(
                "tahun_ajaran"
            )

            search = req.get_param(
                "search"
            )

            conn = get_connection()

            cursor = conn.cursor(
                dictionary=True
            )

            query = """
            SELECT
                id,
                siswa_id,
                nis,
                nama_siswa AS nama,
                kelas,
                tahun_ajaran,
                bulan,
                jumlah_bayar,
                status,
                tanggal_bayar
            FROM pembayaran
            WHERE 1=1
            """

            params = []

            # =========================
            # FILTER TAHUN AJARAN
            # =========================

            if tahun:

                query += """
                AND tahun_ajaran = %s
                """

                params.append(tahun)

            # =========================
            # FILTER SEARCH
            # =========================

            if search:

                query += """
                AND (
                    nis LIKE %s
                    OR nama_siswa LIKE %s
                )
                """

                params.append(
                    f"%{search}%"
                )

                params.append(
                    f"%{search}%"
                )

            query += """
            ORDER BY id DESC
            """

            print("QUERY:", query)
            print("PARAMS:", params)

            cursor.execute(
                query,
                params
            )

            rows = cursor.fetchall()

            resp.media = rows

            resp.status = (
                falcon.HTTP_200
            )

        except Exception as e:

            traceback.print_exc()

            resp.media = {
                "success": False,
                "message": str(e)
            }

            resp.status = (
                falcon.HTTP_500
            )

        finally:

            if cursor:
                cursor.close()

            if conn:
                conn.close()


# =====================================================
# CREATE PEMBAYARAN
# =====================================================

class BayarTagihanCreateResource:

    def on_post(self, req, resp):

        conn = None
        cursor = None

        try:

            body = req.media

            conn = get_connection()

            cursor = conn.cursor()

            cursor.execute("""
            INSERT INTO pembayaran (

                siswa_id,
                nis,
                nama_siswa,
                kelas,
                jenis_pembayaran_id,
                bulan,
                tahun_ajaran,
                jumlah_bayar,
                status,
                tanggal_bayar

            )
            VALUES (
                %s,%s,%s,%s,%s,
                %s,%s,%s,%s,%s
            )
            """, (

                body["siswa_id"],
                body["nis"],
                body["nama_siswa"],
                body["kelas"],
                body["jenis_pembayaran_id"],
                body["bulan"],
                body["tahun_ajaran"],
                body["jumlah_bayar"],
                body.get(
                    "status",
                    "Belum Lunas"
                ),
                body.get(
                    "tanggal_bayar"
                )

            ))

            conn.commit()

            resp.media = {
                "success": True,
                "message":
                "Pembayaran berhasil disimpan"
            }

            resp.status = (
                falcon.HTTP_201
            )

        except Exception as e:

            traceback.print_exc()

            if conn:
                conn.rollback()

            resp.media = {
                "success": False,
                "message": str(e)
            }

            resp.status = (
                falcon.HTTP_500
            )

        finally:

            if cursor:
                cursor.close()

            if conn:
                conn.close()


# =====================================================
# DELETE PEMBAYARAN
# =====================================================

class BayarTagihanByIdResource:

    def on_delete(
        self,
        req,
        resp,
        id
    ):

        conn = None
        cursor = None

        try:

            conn = get_connection()

            cursor = conn.cursor()

            cursor.execute("""
            DELETE FROM pembayaran
            WHERE id = %s
            """, (id,))

            conn.commit()

            resp.media = {
                "success": True,
                "message":
                "Data pembayaran berhasil dihapus"
            }

            resp.status = (
                falcon.HTTP_200
            )

        except Exception as e:

            traceback.print_exc()

            if conn:
                conn.rollback()

            resp.media = {
                "success": False,
                "message": str(e)
            }

            resp.status = (
                falcon.HTTP_500
            )

        finally:

            if cursor:
                cursor.close()

            if conn:
                conn.close()

