import falcon
import random

from models.connection import get_connection


class DataBukuResource:

    # =========================
    # GET ALL
    # =========================
    def on_get(self, req, resp):

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
        SELECT *
        FROM data_buku
        ORDER BY id DESC
        """)

        data = cursor.fetchall()

        cursor.close()
        conn.close()

        resp.media = data


    # =========================
    # INSERT
    # =========================
def on_post(self, req, resp):

    data = req.media

    conn = get_connection()

    cursor = conn.cursor()

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

        # =========================
        # CEK STOK
        # =========================

        cursor.execute("""
        SELECT stok
        FROM data_buku
        WHERE id = %s
        """, (item["buku_id"],))

        buku = cursor.fetchone()

        stok = buku[0]

        qty = item.get("qty", 1)

        if stok < qty:

            resp.status = falcon.HTTP_400

            resp.media = {
                "message": f"Stok buku tidak cukup untuk {item['judul_buku']}"
            }

            cursor.close()
            conn.close()

            return

        # =========================
        # INSERT DETAIL
        # =========================

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
            qty
        ))

        # =========================
        # UPDATE STOK
        # =========================

        cursor.execute("""
        UPDATE data_buku
        SET stok = stok - %s
        WHERE id = %s
        """, (
            qty,
            item["buku_id"]
        ))

    conn.commit()

    cursor.close()
    conn.close()

    resp.media = {
        "message": "Peminjaman buku berhasil",
        "kode_peminjaman": kode_peminjaman
    }


class DataBukuByIdResource:

    # =========================
    # GET BY ID
    # =========================
    def on_get(self, req, resp, id):

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
        SELECT *
        FROM data_buku
        WHERE id = %s
        """, (id,))

        data = cursor.fetchone()

        cursor.close()
        conn.close()

        resp.media = data


    # =========================
    # UPDATE
    # =========================
    def on_put(self, req, resp, id):

        data = req.media

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE data_buku
        SET
            judul = %s,
            isbn = %s,
            penulis = %s,
            penerbit = %s,
            tahun = %s,
            harga = %s,
            kondisi = %s,
            kategori = %s,
            rak = %s,
            stok = %s
        WHERE id = %s
        """, (
            data["judul"],
            data.get("isbn", ""),
            data.get("penulis", ""),
            data.get("penerbit", ""),
            data.get("tahun", 0),
            data.get("harga", 0),
            data.get("kondisi", "Baik"),
            data.get("kategori", ""),
            data.get("rak", ""),
            data.get("stok", 0),
            id
        ))

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message": "Data buku berhasil diupdate"
        }


    # =========================
    # DELETE
    # =========================
    def on_delete(self, req, resp, id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        DELETE FROM data_buku
        WHERE id = %s
        """, (id,))

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message": "Data buku berhasil dihapus"
        }