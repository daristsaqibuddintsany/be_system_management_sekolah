import falcon
from models.connection import get_connection


class RekapitulasiAPBSResource:

    # =====================================================
    # GET REKAP APBS
    # =====================================================

    def on_get(self, req, resp):

        tahun = req.get_param("tahun")

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # =====================================================
        # PENDAPATAN
        # =====================================================

        query_pendapatan = """
        SELECT
            kode_akun AS kode,
            nama_akun AS nama,
            SUM(nominal) AS realisasi
        FROM realisasi_penerimaan
        WHERE 1=1
        """

        values_pendapatan = []

        if tahun:

            query_pendapatan += """
            AND tahun_ajaran=%s
            """

            values_pendapatan.append(tahun)

        query_pendapatan += """
        GROUP BY kode_akun, nama_akun
        ORDER BY kode_akun ASC
        """

        cursor.execute(
            query_pendapatan,
            tuple(values_pendapatan)
        )

        pendapatan = cursor.fetchall()

        # =====================================================
        # BELANJA
        # =====================================================

        query_belanja = """
        SELECT
            kode_akun AS kode,
            nama_akun AS nama,
            SUM(nominal) AS realisasi
        FROM realisasi_belanja
        WHERE 1=1
        """

        values_belanja = []

        if tahun:

            query_belanja += """
            AND tahun_ajaran=%s
            """

            values_belanja.append(tahun)

        query_belanja += """
        GROUP BY kode_akun, nama_akun
        ORDER BY kode_akun ASC
        """

        cursor.execute(
            query_belanja,
            tuple(values_belanja)
        )

        belanja = cursor.fetchall()

        # =====================================================
        # FORMAT DATA
        # =====================================================

        data_pendapatan = []

        for i, item in enumerate(pendapatan, start=1):

            realisasi = int(item["realisasi"] or 0)

            data_pendapatan.append({
                "no": i,
                "kode": item["kode"],
                "nama": item["nama"],
                "realisasi": realisasi,
                "saldo_awal": 0,
                "saldo_berjalan": realisasi,
                "proyeksi_akhir_tahun": realisasi
            })

        data_belanja = []

        start_no = len(data_pendapatan) + 1

        for i, item in enumerate(
            belanja,
            start=start_no
        ):

            realisasi = int(item["realisasi"] or 0)

            data_belanja.append({
                "no": i,
                "kode": item["kode"],
                "nama": item["nama"],
                "realisasi": realisasi,
                "saldo_awal": 0,
                "saldo_berjalan": realisasi,
                "proyeksi_akhir_tahun": realisasi
            })

        # =====================================================
        # TOTAL
        # =====================================================

        total_pendapatan = sum(
            item["realisasi"]
            for item in data_pendapatan
        )

        total_belanja = sum(
            item["realisasi"]
            for item in data_belanja
        )

        total_keseluruhan = (
            total_pendapatan +
            total_belanja
        )

        cursor.close()
        conn.close()

        resp.media = {

            "pendapatan": data_pendapatan,

            "belanja": data_belanja,

            "total_pendapatan": total_pendapatan,

            "total_belanja": total_belanja,

            "total_keseluruhan": total_keseluruhan

        }

        resp.status = falcon.HTTP_200