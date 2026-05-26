import falcon
from models.connection import get_connection


class APBDDetailResource:

    # =====================================================
    # GET APBD DETAIL
    # =====================================================

    def on_get(self, req, resp):

        tahun = req.get_param("tahun")

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        bulan_urutan = [
            "Juli",
            "Agustus",
            "September",
            "Oktober",
            "November",
            "Desember",
            "Januari",
            "Februari",
            "Maret",
            "April",
            "Mei",
            "Juni"
        ]

        # =====================================================
        # FUNCTION FORMAT DATA
        # =====================================================

        def get_data(table_name):

            query = f"""
            SELECT
                kode_akun,
                nama_akun,
                bulan,
                SUM(nominal) AS total
            FROM {table_name}
            WHERE 1=1
            """

            values = []

            if tahun:

                query += """
                AND tahun_ajaran=%s
                """

                values.append(tahun)

            query += """
            GROUP BY
                kode_akun,
                nama_akun,
                bulan

            ORDER BY
                kode_akun ASC
            """

            cursor.execute(query, tuple(values))

            raw = cursor.fetchall()

            hasil = {}

            for row in raw:

                kode = row["kode_akun"]

                if kode not in hasil:

                    hasil[kode] = {
                        "kode": kode,
                        "nama": row["nama_akun"],
                        "bulan": [0] * 12,
                        "total": 0
                    }

                bulan_index = bulan_urutan.index(
                    row["bulan"]
                )

                nominal = int(row["total"] or 0)

                hasil[kode]["bulan"][bulan_index] = nominal

                hasil[kode]["total"] += nominal

            return list(hasil.values())

        # =====================================================
        # DATA
        # =====================================================

        pendapatan = get_data(
            "realisasi_penerimaan"
        )

        belanja = get_data(
            "realisasi_belanja"
        )

        # =====================================================
        # TOTAL PENDAPATAN
        # =====================================================

        total_pendapatan_bulan = [0] * 12

        for item in pendapatan:

            for i in range(12):

                total_pendapatan_bulan[i] += (
                    item["bulan"][i]
                )

        total_pendapatan = sum(
            total_pendapatan_bulan
        )

        # =====================================================
        # TOTAL BELANJA
        # =====================================================

        total_belanja_bulan = [0] * 12

        for item in belanja:

            for i in range(12):

                total_belanja_bulan[i] += (
                    item["bulan"][i]
                )

        total_belanja = sum(
            total_belanja_bulan
        )

        # =====================================================
        # GRAND TOTAL
        # =====================================================

        grand_total_bulan = [
            total_pendapatan_bulan[i] +
            total_belanja_bulan[i]
            for i in range(12)
        ]

        grand_total = sum(
            grand_total_bulan
        )

        cursor.close()
        conn.close()

        resp.media = {

            "pendapatan": pendapatan,

            "belanja": belanja,

            "total_pendapatan_bulan":
                total_pendapatan_bulan,

            "total_pendapatan":
                total_pendapatan,

            "total_belanja_bulan":
                total_belanja_bulan,

            "total_belanja":
                total_belanja,

            "grand_total_bulan":
                grand_total_bulan,

            "grand_total":
                grand_total
        }

        resp.status = falcon.HTTP_200