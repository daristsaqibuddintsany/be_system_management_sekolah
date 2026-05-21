import falcon
from models.connection import get_connection


class RiwayatTabunganResource:

    # =========================
    # GET RIWAYAT TABUNGAN
    # =========================
    def on_get(self, req, resp):

        search = req.get_param("search")
        tanggal_awal = req.get_param("tanggal_awal")
        tanggal_akhir = req.get_param("tanggal_akhir")

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT

            id,
            nis,
            jenis,
            nominal AS jumlah,
            keterangan,
            DATE(created_at) AS tanggal

        FROM transaksi_tabungan_teller

        WHERE 1=1
        """

        values = []

        # =========================
        # FILTER SEARCH
        # =========================

        if search:

            query += """
            AND (
                nis LIKE %s
            )
            """

            values.append(f"%{search}%")

        # =========================
        # FILTER TANGGAL
        # =========================

        if tanggal_awal and tanggal_akhir:

            query += """
            AND DATE(created_at)
            BETWEEN %s AND %s
            """

            values.append(tanggal_awal)
            values.append(tanggal_akhir)

        query += """
        ORDER BY created_at DESC
        """

        cursor.execute(query, tuple(values))

        rows = cursor.fetchall()

        # =========================
        # FORMAT JENIS
        # =========================

        result = []

        for item in rows:

            result.append({

                "id": item["id"],
                "nis": item["nis"],
                "nama": "-",  # bisa diganti join siswa
                "tanggal": str(item["tanggal"]),

                "jenis":
                    "Setor"
                    if item["jenis"] == "Penyetoran"
                    else "Tarik",

                "jumlah": item["jumlah"],

                "keterangan": item["keterangan"]

            })

        cursor.close()
        conn.close()

        resp.media = {
            "data": result
        }

        resp.status = falcon.HTTP_200