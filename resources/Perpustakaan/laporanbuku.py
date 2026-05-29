import falcon

from models.connection import get_connection


class LaporanBukuResource:

    # =========================
    # GET LAPORAN STOK BUKU
    # =========================
    def on_get(self, req, resp):

        conn = get_connection()

        cursor = conn.cursor(dictionary=True)

        # =========================
        # QUERY LAPORAN
        # =========================

        cursor.execute("""
        SELECT
            db.id,
            db.judul_buku AS judul,
            db.isbn,
            db.penulis,
            db.tahun_terbit AS tahun,
            db.kategori,
            db.stok AS stokTotal,

            COALESCE(
                (
                    SELECT SUM(pbd.qty)
                    FROM peminjaman_buku_detail pbd
                    INNER JOIN peminjaman_buku pb
                    ON pb.id = pbd.peminjaman_id
                    WHERE pbd.buku_id = db.id
                    AND pb.status = 'Dipinjam'
                ), 0
            ) AS dipinjam,

            (
                db.stok -
                COALESCE(
                    (
                        SELECT SUM(pbd.qty)
                        FROM peminjaman_buku_detail pbd
                        INNER JOIN peminjaman_buku pb
                        ON pb.id = pbd.peminjaman_id
                        WHERE pbd.buku_id = db.id
                        AND pb.status = 'Dipinjam'
                    ), 0
                )
            ) AS tersedia

        FROM data_buku db

        ORDER BY db.id DESC
        """)

        data = cursor.fetchall()

        cursor.close()
        conn.close()

        resp.media = data