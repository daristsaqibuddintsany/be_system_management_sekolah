import falcon
from models.connection import get_connection

class TransaksiJurnalResource:

    # ==========================================
    # GET ALL JURNAL + DETAIL BARISNYA
    # ==========================================
    def on_get(self, req, resp):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # 1. Ambil semua data induk jurnal
        cursor.execute("SELECT id, DATE_FORMAT(tanggal, '%Y-%m-%d') as tanggal, keperluan FROM jurnal ORDER BY id DESC")
        jurnal_list = cursor.fetchall()

        # 2. Ambil detail akun untuk setiap jurnal
        for index, jrl in enumerate(jurnal_list):
            cursor.execute("""
                SELECT jd.akun_id, jd.debit, jd.kredit, a.nama_akun
                FROM jurnal_detail jd
                JOIN akun a ON jd.akun_id = a.id
                WHERE jd.jurnal_id = %s
            """, (jrl["id"],))
            
            details = cursor.fetchall()
            
            # Konversi tipe data numeric agar aman di-serialize ke JSON
            formatted_details = []
            for d in details:
                formatted_details.append({
                    "akun_id": d["akun_id"],
                    "nama_akun": d["nama_akun"],
                    "debit": int(d["debit"]),
                    "kredit": int(d["kredit"])
                })
            
            jurnal_list[index]["detail"] = formatted_details

        cursor.close()
        conn.close()

        resp.media = jurnal_list
        resp.status = falcon.HTTP_200

    # ==========================================
    # CREATE TRANSAKSI JURNAL (PARENT & DETAILS)
    # ==========================================
    def on_post(self, req, resp):
        body = req.media or {}
        tanggal = body.get("tanggal")
        keperluan = body.get("keperluan")
        detail = body.get("detail", [])

        if not tanggal or not keperluan or not detail:
            raise falcon.HTTPBadRequest(title="Validation Error", description="Form induk dan baris akun wajib diisi.")

        conn = get_connection()
        cursor = conn.cursor()

        try:
            # Ganti auto-commit ke False untuk keamanan data relasional
            conn.autocommit = False

            # 1. Insert ke tabel induk (jurnal)
            cursor.execute(
                "INSERT INTO jurnal (tanggal, keperluan) VALUES (%s, %s)",
                (tanggal, keperluan)
            )
            jurnal_id = cursor.lastrowid

            # 2. Insert semua baris detail akun
            for item in detail:
                cursor.execute("""
                    INSERT INTO jurnal_detail (jurnal_id, akun_id, debit, kredit)
                    VALUES (%s, %s, %s, %s)
                """, (jurnal_id, item.get("akun_id"), item.get("debit", 0), item.get("kredit", 0)))

            # Jika semua baris sukses, commit ke database
            conn.commit()
            
            resp.media = {"message": "Transaksi jurnal berhasil disimpan"}
            resp.status = falcon.HTTP_201

        except Exception as e:
            conn.rollback() # Batalkan semua jika ada yang gagal insert
            raise falcon.HTTPBadRequest(title="Database Error", description=str(e))
        finally:
            cursor.close()
            conn.close()


class TransaksiJurnalByIdResource:

    # ==========================================
    # UPDATE TRANSAKSI JURNAL
    # ==========================================
    def on_put(self, req, resp, id):
        body = req.media or {}
        tanggal = body.get("tanggal")
        keperluan = body.get("keperluan")
        detail = body.get("detail", [])

        conn = get_connection()
        cursor = conn.cursor()

        try:
            conn.autocommit = False

            # 1. Update data induk jurnal
            cursor.execute(
                "UPDATE jurnal SET tanggal=%s, keperluan=%s WHERE id=%s",
                (tanggal, keperluan, id)
            )

            # 2. Hapus detail lama, lalu tulis ulang dengan detail baru (cara paling aman & bersih)
            cursor.execute("DELETE FROM jurnal_detail WHERE jurnal_id=%s", (id,))
            
            for item in detail:
                cursor.execute("""
                    INSERT INTO jurnal_detail (jurnal_id, akun_id, debit, kredit)
                    VALUES (%s, %s, %s, %s)
                """, (id, item.get("akun_id"), item.get("debit", 0), item.get("kredit", 0)))

            conn.commit()
            resp.media = {"message": "Transaksi jurnal berhasil diupdate"}
            resp.status = falcon.HTTP_200

        except Exception as e:
            conn.rollback()
            raise falcon.HTTPBadRequest(title="Database Error", description=str(e))
        finally:
            cursor.close()
            conn.close()

    # ==========================================
    # DELETE TRANSAKSI JURNAL
    # ==========================================
    def on_delete(self, req, resp, id):
        conn = get_connection()
        cursor = conn.cursor()

        # Karena tabel detail menggunakan ON DELETE CASCADE, 
        # menghapus data di induk jurnal otomatis menghapus baris di jurnal_detail.
        cursor.execute("DELETE FROM jurnal WHERE id=%s", (id,))
        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {"message": "Transaksi jurnal berhasil dihapus"}
        resp.status = falcon.HTTP_200