import falcon

from models.connection import get_connection


class LaporanPeminjamanResource:

    # =========================
    # GET LAPORAN PEMINJAMAN
    # =========================
    def on_get(self, req, resp):

        conn = get_connection()

        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
        SELECT
            lp.id,
            lp.nama_anggota AS nama,
            lp.judul_buku AS buku,
            lp.tanggal_pinjam AS tanggalPinjam,
            lp.tanggal_kembali AS tanggalKembali,
            lp.status

        FROM laporan_peminjaman lp

        ORDER BY lp.id DESC
        """)

        data = cursor.fetchall()

        cursor.close()
        conn.close()

        resp.media = data