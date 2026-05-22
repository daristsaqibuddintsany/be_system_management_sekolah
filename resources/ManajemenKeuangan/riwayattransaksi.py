import falcon
from models.connection import get_connection


class RiwayatTransaksiResource:

    # =========================
    # GET RIWAYAT TRANSAKSI
    # =========================
    def on_get(self, req, resp):

        tanggal_awal = req.get_param("tanggal_awal")
        tanggal_akhir = req.get_param("tanggal_akhir")

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT

            ttt.id,
            ttt.nis,

            COALESCE(
                s.nama_siswa,
                '-'
            ) AS nama,

            ttt.jenis,

            ttt.nominal AS jumlah,

            ttt.keterangan,

            DATE(ttt.created_at) AS tanggal

        FROM transaksi_tabungan_teller ttt

        LEFT JOIN data_siswa s
        ON s.nis = ttt.nis

        WHERE 1=1
        """

        values = []

        # =========================
        # FILTER TANGGAL
        # =========================

        if tanggal_awal and tanggal_akhir:

            query += """
            AND DATE(ttt.created_at)
            BETWEEN %s AND %s
            """

            values.append(tanggal_awal)
            values.append(tanggal_akhir)

        query += """
        ORDER BY ttt.created_at DESC
        """

        cursor.execute(query, tuple(values))

        rows = cursor.fetchall()

        result = []

        for i, item in enumerate(rows):

            result.append({

                "id": item["id"],

                "kode": f"TRX-{item['id']}",

                "tanggal": str(item["tanggal"]),

                "jenis":
                    "Setor"
                    if item["jenis"] == "Penyetoran"
                    else "Tarik",

                "nis": item["nis"],

                "nama": item["nama"],

                "jumlah": item["jumlah"],

                "keterangan": item["keterangan"]

            })

        cursor.close()
        conn.close()

        resp.media = result

        resp.status = falcon.HTTP_200