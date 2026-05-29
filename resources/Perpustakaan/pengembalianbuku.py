import falcon
import random
from datetime import datetime

from models.connection import get_connection


class PengembalianBukuResource:

    # =========================
    # GET ALL
    # =========================
    def on_get(self, req, resp):

        conn = get_connection()

        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
        SELECT *
        FROM pengembalian_buku
        ORDER BY id DESC
        """)

        data = cursor.fetchall()

        for item in data:

            cursor.execute("""
            SELECT *
            FROM pengembalian_buku_detail
            WHERE pengembalian_id = %s
            """, (item["id"],))

            item["detail_buku"] = cursor.fetchall()

        cursor.close()
        conn.close()

        resp.media = data


    # =========================
    # INSERT PENGEMBALIAN
    # =========================
    def on_post(self, req, resp):

        data = req.media

        conn = get_connection()

        cursor = conn.cursor(dictionary=True)

        kode_pengembalian = "KMB" + str(
            random.randint(100000, 999999)
        )

        # =========================
        # CEK DATA PEMINJAMAN
        # =========================

        cursor.execute("""
        SELECT *
        FROM peminjaman_buku
        WHERE id = %s
        """, (data["peminjaman_id"],))

        peminjaman = cursor.fetchone()

        if not peminjaman:

            resp.status = falcon.HTTP_404

            resp.media = {
                "message": "Data peminjaman tidak ditemukan"
            }

            return

        # =========================
        # HITUNG DENDA
        # =========================

        tanggal_kembali = datetime.strptime(
            str(peminjaman["tanggal_kembali"]),
            "%Y-%m-%d"
        )

        tanggal_dikembalikan = datetime.strptime(
            data["tanggal_dikembalikan"],
            "%Y-%m-%d"
        )

        selisih = (
            tanggal_dikembalikan - tanggal_kembali
        ).days

        total_denda = 0

        status = "Dikembalikan"

        if selisih > 0:

            total_denda = selisih * 1000

            status = "Terlambat"

        # =========================
        # INSERT HEADER
        # =========================

        cursor.execute("""
        INSERT INTO pengembalian_buku (
            peminjaman_id,
            kode_pengembalian,
            kode_peminjaman,
            anggota_id,
            nama_anggota,
            tanggal_pinjam,
            tanggal_kembali,
            tanggal_dikembalikan,
            total_buku,
            total_denda,
            status,
            catatan
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            peminjaman["id"],
            kode_pengembalian,
            peminjaman["kode_peminjaman"],
            peminjaman["anggota_id"],
            peminjaman["nama_anggota"],
            peminjaman["tanggal_pinjam"],
            peminjaman["tanggal_kembali"],
            data["tanggal_dikembalikan"],
            peminjaman["total_buku"],
            total_denda,
            status,
            data.get("catatan", "")
        ))

        conn.commit()

        pengembalian_id = cursor.lastrowid

        # =========================
        # AMBIL DETAIL PINJAMAN
        # =========================

        cursor.execute("""
        SELECT *
        FROM peminjaman_buku_detail
        WHERE peminjaman_id = %s
        """, (peminjaman["id"],))

        detail = cursor.fetchall()

        # =========================
        # INSERT DETAIL
        # =========================

        for item in detail:

            cursor.execute("""
            INSERT INTO pengembalian_buku_detail (
                pengembalian_id,
                buku_id,
                barcode,
                judul_buku,
                qty
            ) VALUES (%s, %s, %s, %s, %s)
            """, (
                pengembalian_id,
                item["buku_id"],
                item["barcode"],
                item["judul_buku"],
                item["qty"]
            ))

            # =========================
            # KEMBALIKAN STOK
            # =========================

            cursor.execute("""
            UPDATE data_buku
            SET stok = stok + %s
            WHERE id = %s
            """, (
                item["qty"],
                item["buku_id"]
            ))

        # =========================
        # UPDATE STATUS PEMINJAMAN
        # =========================

        cursor.execute("""
        UPDATE peminjaman_buku
        SET status = 'Dikembalikan'
        WHERE id = %s
        """, (peminjaman["id"],))

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message": "Buku berhasil dikembalikan",
            "kode_pengembalian": kode_pengembalian,
            "total_denda": total_denda
        }


class PengembalianBukuByIdResource:

    # =========================
    # GET DETAIL
    # =========================
    def on_get(self, req, resp, id):

        conn = get_connection()

        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
        SELECT *
        FROM pengembalian_buku
        WHERE id = %s
        """, (id,))

        data = cursor.fetchone()

        cursor.execute("""
        SELECT *
        FROM pengembalian_buku_detail
        WHERE pengembalian_id = %s
        """, (id,))

        data["detail_buku"] = cursor.fetchall()

        cursor.close()
        conn.close()

        resp.media = data