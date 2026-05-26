import falcon
from models.connection import get_connection


class LaporanJurnalResource:

    # ==========================================
    # GET DATA UNTUK LAPORAN JURNAL (FLAT STRUCTURE)
    # ==========================================
    def on_get(self, req, resp):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # Melakukan JOIN untuk meratakan data induk dan detail menjadi 1 baris per akun
        # Kolom 'petugas' di-set string kosong atau nama akun sebagai pelengkap agar filter FE tidak error
        cursor.execute("""
            SELECT 
                j.id as id,
                CONCAT('JRL-', LPAD(j.id, 5, '0')) as kode, 
                DATE_FORMAT(j.tanggal, '%Y-%m-%d') as tanggal,
                CONCAT(j.keperluan, ' (', a.nama_akun, ')') as keperluan,
                a.nama_akun as petugas, -- Diarahkan ke nama_akun agar pencarian 'petugas' di FE berfungsi mencari nama akun
                jd.debit as debit,
                jd.kredit as kredit
            FROM jurnal j
            INNER JOIN jurnal_detail jd ON j.id = jd.jurnal_id
            INNER JOIN akun a ON jd.akun_id = a.id
            ORDER BY j.tanggal DESC, j.id DESC, jd.id ASC
        """)
        
        data = cursor.fetchall()
        
        # Konversi data numeric agar bisa di-serialize ke JSON dengan aman
        for row in data:
            row["debit"] = float(row["debit"]) if row["debit"] else 0.0
            row["kredit"] = float(row["kredit"]) if row["kredit"] else 0.0

        cursor.close()
        conn.close()

        # Response langsung berupa array [] sesuai dengan state data di FE Anda
        resp.media = data
        resp.status = falcon.HTTP_200


class LaporanJurnalByIdResource:

    # ==========================================
    # ACTION DETACH / DELETE DARI LAPORAN
    # ==========================================
    def on_delete(self, req, resp, id):
        conn = get_connection()
        cursor = conn.cursor()

        # Menghapus data induk otomatis menghapus detail karena ON DELETE CASCADE
        cursor.execute("DELETE FROM jurnal WHERE id = %s", (id,))
        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {"message": "Data transaksi jurnal berhasil dihapus"}
        resp.status = falcon.HTTP_200

    # ==========================================
    # ACTION UPDATE DARI LAPORAN (BASIC SHORTCUT)
    # ==========================================
    def on_put(self, req, resp, id):
        body = req.media or {}
        tanggal = body.get("tanggal")
        # Mengembalikan string keperluan murni (memotong teks nama akun di dalam kurung jika ada)
        keperluan = body.get("keperluan", "").split(" (")[0] 

        conn = get_connection()
        cursor = conn.cursor()

        # Update data induknya saja melalui baris laporan
        cursor.execute("""
            UPDATE jurnal 
            SET tanggal = %s, keperluan = %s 
            WHERE id = %s
        """, (tanggal, keperluan, id))

        conn.commit()
        cursor.close()
        conn.close()

        resp.media = {"message": "Data jurnal berhasil diupdate"}
        resp.status = falcon.HTTP_200