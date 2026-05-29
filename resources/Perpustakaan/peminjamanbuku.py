import falcon
import random
from datetime import datetime

from models.connection import get_connection


class PeminjamanBukuResource:

    # =========================
    # GET ALL
    # =========================
    def on_get(self, req, resp):

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
        SELECT *
        FROM peminjaman_buku
        ORDER BY id DESC
        """)

        data = cursor.fetchall()

        for item in data:

            cursor.execute("""
            SELECT *
            FROM peminjaman_buku_detail
            WHERE peminjaman_id = %s
            """, (item["id"],))

            item["detail_buku"] = cursor.fetchall()

        cursor.close()
        conn.close()

        resp.media = data


    # =========================
    # INSERT PEMINJAMAN
    # =========================
    def on_post(self, req, resp):

        data = req.media

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        kode_peminjaman = "PJM" + str(
            random.randint(100000, 999999)
        )

        # =========================
        # INSERT HEADER
        # =========================

        cursor.execute("""
        INSERT INTO peminjaman_buku (
            kode_peminjaman,
            anggota_id,
            nama_anggota,
            tanggal_pinjam,
            tanggal_kembali,
            total_buku,
            status,
            catatan
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            kode_peminjaman,
            data["anggota_id"],
            data["nama_anggota"],
            data["tanggal_pinjam"],
            data["tanggal_kembali"],
            len(data["detail_buku"]),
            "Dipinjam",
            data.get("catatan", "")
        ))

        conn.commit()

        peminjaman_id = cursor.lastrowid

        # =========================
        # INSERT DETAIL
        # =========================

        for item in data["detail_buku"]:

            cursor.execute("""
            INSERT INTO peminjaman_buku_detail (
                peminjaman_id,
                buku_id,
                barcode,
                judul_buku,
                qty
            ) VALUES (%s, %s, %s, %s, %s)
            """, (
                peminjaman_id,
                item["buku_id"],
                item.get("barcode", ""),
                item["judul_buku"],
                item.get("qty", 1)
            ))

            # =========================
            # KURANGI STOK BUKU
            # =========================

            cursor.execute("""
            UPDATE data_buku
            SET stok = stok - %s
            WHERE id = %s
            """, (
                item.get("qty", 1),
                item["buku_id"]
            ))

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message": "Peminjaman buku berhasil",
            "kode_peminjaman": kode_peminjaman
        }
        
class PeminjamanBukuByIdResource:

    # =========================
    # GET DETAIL
    # =========================
    def on_get(self, req, resp, id):

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
        SELECT *
        FROM peminjaman_buku
        WHERE id = %s
        """, (id,))

        data = cursor.fetchone()

        cursor.execute("""
        SELECT *
        FROM peminjaman_buku_detail
        WHERE peminjaman_id = %s
        """, (id,))

        detail = cursor.fetchall()

        data["detail_buku"] = detail

        cursor.close()
        conn.close()

        resp.media = data


    # =========================
    # DELETE
    # =========================
    def on_delete(self, req, resp, id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        DELETE FROM peminjaman_buku
        WHERE id = %s
        """, (id,))

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message": "Data peminjaman berhasil dihapus"
        }