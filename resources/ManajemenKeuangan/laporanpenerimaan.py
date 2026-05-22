import falcon
from models.connection import get_connection


class LaporanPenerimaanResource:

    # =========================
    # GET DATA LAPORAN
    # =========================
    def on_get(self, req, resp):

        tanggal_awal = req.get_param("tanggal_awal")
        tanggal_akhir = req.get_param("tanggal_akhir")

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT
            id,
            kode,
            tanggal,
            jenis,
            sumber,
            petugas,
            menyetujui,
            keterangan,
            nominal
        FROM transaksi_pengeluaran
        WHERE 1=1
        """

        values = []

        # FILTER TANGGAL AWAL
        if tanggal_awal:
            query += " AND DATE(tanggal) >= %s"
            values.append(tanggal_awal)

        # FILTER TANGGAL AKHIR
        if tanggal_akhir:
            query += " AND DATE(tanggal) <= %s"
            values.append(tanggal_akhir)

        query += " ORDER BY id DESC"

        cursor.execute(query, tuple(values))

        data = cursor.fetchall()

        cursor.close()
        conn.close()

        resp.media = data
        resp.status = falcon.HTTP_200


class LaporanPenerimaanByIdResource:

    # =========================
    # DELETE
    # =========================
    def on_delete(self, req, resp, id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        DELETE FROM transaksi_pengeluaran
        WHERE id=%s
        """, (id,))

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message": "Data laporan berhasil dihapus"
        }

        resp.status = falcon.HTTP_200