import falcon
from models.connection import get_connection


class RekapSiswaResource:

    # =========================================
    # GET DATA REKAP SISWA
    # =========================================
    def on_get(self, req, resp):

        kelas = req.get_param("kelas")
        tahun = req.get_param("tahun")

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT

            p.siswa_id AS id,

            p.nis,

            p.nama_siswa AS nama,

            p.kelas,

            p.tahun_ajaran AS tahun,

            SUM(p.jumlah_tagihan) AS total_tagihan,

            SUM(p.jumlah_bayar) AS total_bayar,

            SUM(p.sisa_tagihan) AS total_tunggakan

        FROM pembayaran p

        WHERE 1=1
        """

        values = []

        # =========================================
        # FILTER KELAS
        # =========================================
        if kelas:
            query += """
            AND p.kelas=%s
            """
            values.append(kelas)

        # =========================================
        # FILTER TAHUN
        # =========================================
        if tahun:
            query += """
            AND p.tahun_ajaran=%s
            """
            values.append(tahun)

        query += """
        GROUP BY
            p.siswa_id,
            p.nis,
            p.nama_siswa,
            p.kelas,
            p.tahun_ajaran

        ORDER BY p.nama_siswa ASC
        """

        cursor.execute(query, tuple(values))

        data = cursor.fetchall()

        cursor.close()
        conn.close()

        resp.media = {
            "data": data
        }

        resp.status = falcon.HTTP_200


class RekapSiswaByIdResource:

    # =========================================
    # DETAIL REKAP SISWA
    # =========================================
    def on_get(self, req, resp, id):

        tahun = req.get_param("tahun")

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # =========================================
        # IDENTITAS SISWA
        # =========================================
        query_siswa = """
        SELECT

            siswa_id,

            nis,

            nama_siswa,

            kelas,

            tahun_ajaran

        FROM pembayaran

        WHERE siswa_id=%s
        """

        values_siswa = [id]

        if tahun:
            query_siswa += """
            AND tahun_ajaran=%s
            """
            values_siswa.append(tahun)

        query_siswa += """
        LIMIT 1
        """

        cursor.execute(
            query_siswa,
            tuple(values_siswa)
        )

        siswa = cursor.fetchone()

        # =========================================
        # VALIDASI DATA
        # =========================================
        if not siswa:

            cursor.close()
            conn.close()

            resp.media = {
                "message": "Data siswa tidak ditemukan"
            }

            resp.status = falcon.HTTP_404
            return

        # =========================================
        # DETAIL PEMBAYARAN
        # =========================================
        query_detail = """
        SELECT

            p.id,

            p.bulan,

            jp.nama AS jenis_pembayaran,

            p.jumlah_tagihan,

            p.jumlah_bayar,

            p.sisa_tagihan,

            p.status,

            p.tanggal_bayar

        FROM pembayaran p

        JOIN jenis_pembayaran jp
        ON jp.id = p.jenis_pembayaran_id

        WHERE p.siswa_id=%s
        """

        values_detail = [id]

        if tahun:
            query_detail += """
            AND p.tahun_ajaran=%s
            """
            values_detail.append(tahun)

        query_detail += """
        ORDER BY p.id DESC
        """

        cursor.execute(
            query_detail,
            tuple(values_detail)
        )

        pembayaran = cursor.fetchall()

        # =========================================
        # SUMMARY
        # =========================================
        query_summary = """
        SELECT

            SUM(jumlah_tagihan) AS total_tagihan,

            SUM(jumlah_bayar) AS total_bayar,

            SUM(sisa_tagihan) AS total_tunggakan

        FROM pembayaran

        WHERE siswa_id=%s
        """

        values_summary = [id]

        if tahun:
            query_summary += """
            AND tahun_ajaran=%s
            """
            values_summary.append(tahun)

        cursor.execute(
            query_summary,
            tuple(values_summary)
        )

        summary = cursor.fetchone()

        cursor.close()
        conn.close()

        # =========================================
        # RESPONSE
        # =========================================
        resp.media = {

            "id": siswa["siswa_id"],

            "nis": siswa["nis"],

            "nama": siswa["nama_siswa"],

            "kelas": siswa["kelas"],

            "tahun": siswa["tahun_ajaran"],

            "pembayaran": pembayaran,

            "summary": summary

        }

        resp.status = falcon.HTTP_200