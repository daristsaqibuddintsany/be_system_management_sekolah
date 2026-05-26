import falcon
from datetime import datetime
from models.connection import get_connection


class TransaksiPengeluaranResource:

    # =========================
    # GET ALL TRANSAKSI
    # =========================
    def on_get(self, req, resp):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # Mengambil data diurutkan dari yang terbaru dan mengubah format tanggal menjadi string ISO (YYYY-MM-DD)
        cursor.execute("""
            SELECT 
                id, kode, jenis, bidang, penerima, sumber, 
                DATE_FORMAT(tanggal, '%Y-%m-%d') as tanggal, 
                menyetujui, keterangan, nominal
            FROM transaksi_pengeluaran
            ORDER BY id DESC
        """)
        
        data = cursor.fetchall()
        
        # Konversi tipe data DECIMAL ke float/int agar bisa di-serialize ke JSON
        for row in data:
            if row["nominal"]:
                row["nominal"] = float(row["nominal"])

        cursor.close()
        conn.close()

        resp.media = data
        resp.status = falcon.HTTP_200

    # =========================
    # CREATE TRANSAKSI
    # =========================
    def on_post(self, req, resp):
        body = req.media or {}

        # Validasi field wajib sesuai handling di Frontend
        if not body.get("jenis") or not body.get("tanggal") or not body.get("nominal"):
            raise falcon.HTTPBadRequest(
                title="Missing fields",
                description="Field 'jenis', 'tanggal', dan 'nominal' wajib diisi."
            )

        conn = get_connection()
        cursor = conn.cursor()

        # --- LOGIKA AUTO GENERATE KODE TRANSAKSI ---
        # Contoh Format: OUT-YYYYMM-0001
        current_year_month = datetime.now().strftime("%Y%m")
        prefix = f"OUT-{current_year_month}-"
        
        cursor.execute(
            "SELECT kode FROM transaksi_pengeluaran WHERE kode LIKE %s ORDER BY id DESC LIMIT 1",
            (f"{prefix}%",)
        )
        last_code = cursor.fetchone()

        if last_code:
            last_number = int(last_code[0].split("-")[-1])
            new_number = str(last_number + 1).zfill(4)
        else:
            new_number = "0001"
            
        generated_kode = f"{prefix}{new_number}"
        # -------------------------------------------

        cursor.execute("""
            INSERT INTO transaksi_pengeluaran (
                kode, jenis, bidang, penerima, sumber, tanggal, menyetujui, keterangan, nominal
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            generated_kode,
            body.get("jenis"),
            body.get("bidang"),
            body.get("penerima"),
            body.get("sumber"),
            body.get("tanggal"),  # Menerima format YYYY-MM-DD dari FE
            body.get("menyetujui"),
            body.get("keterangan"),
            body.get("nominal")
        ))

        conn.commit()
        cursor.close()
        conn.close()

        resp.media = {
            "message": "Transaksi pengeluaran berhasil disimpan",
            "kode": generated_kode
        }
        resp.status = falcon.HTTP_201


class TransaksiPengeluaranByIdResource:

    # =========================
    # UPDATE TRANSAKSI
    # =========================
    def on_put(self, req, resp, id):
        body = req.media or {}

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE transaksi_pengeluaran
            SET
                jenis=%s,
                bidang=%s,
                penerima=%s,
                sumber=%s,
                tanggal=%s,
                menyetujui=%s,
                keterangan=%s,
                nominal=%s
            WHERE id=%s
        """, (
            body.get("jenis"),
            body.get("bidang"),
            body.get("penerima"),
            body.get("sumber"),
            body.get("tanggal"),
            body.get("menyetujui"),
            body.get("keterangan"),
            body.get("nominal"),
            id
        ))

        conn.commit()
        cursor.close()
        conn.close()

        resp.media = {
            "message": "Data transaksi berhasil diupdate"
        }
        resp.status = falcon.HTTP_200

    # =========================
    # DELETE TRANSAKSI
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
            "message": "Data transaksi berhasil dihapus"
        }
        resp.status = falcon.HTTP_200