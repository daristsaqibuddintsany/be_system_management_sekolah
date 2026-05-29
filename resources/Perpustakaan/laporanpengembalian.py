import falcon

from models.connection import get_connection


class LaporanPengembalianResource:

    # =========================
    # GET LAPORAN PENGEMBALIAN
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
            lp.tanggal_dikembalikan AS tanggalKembali,
            lp.total_denda AS denda,
            lp.status

        FROM laporan_pengembalian lp

        ORDER BY lp.id DESC
        """)

        data = cursor.fetchall()

        cursor.close()
        conn.close()

        resp.media = data