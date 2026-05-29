import falcon

from models.connection import get_connection


class LaporanDendaResource:

    # =========================
    # GET LAPORAN DENDA
    # =========================
    def on_get(self, req, resp):

        conn = get_connection()

        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
        SELECT
            ld.id,
            ld.nama_anggota AS nama,
            ld.judul_buku AS buku,
            ld.tanggal_kembali AS tanggalKembali,
            ld.terlambat_hari AS terlambat,
            ld.total_denda AS denda

        FROM laporan_denda ld

        ORDER BY ld.id DESC
        """)

        data = cursor.fetchall()

        cursor.close()
        conn.close()

        resp.media = data