import falcon
from datetime import datetime
from models.connection import get_connection

class NeracaSaldoResource:

    # ==========================================
    # GET DATA NERACA SALDO (BUKU BESAR RINGKASAN)
    # ==========================================
    def on_get(self, req, resp):
        # 1. Ambil parameter filter tanggal dari query string Axios
        tanggal_awal = req.get_param('tanggal_awal')
        tanggal_akhir = req.get_param('tanggal_akhir')

        # Proteksi jika Frontend mengirim tanggal kosong (fallback ke bulan berjalan)
        if not tanggal_awal or not tanggal_akhir:
            today = datetime.now()
            tanggal_awal = today.replace(day=1).strftime('%Y-%m-%d')
            tanggal_akhir = today.strftime('%Y-%m-%d')

        # 2. Buka koneksi database dengan dictionary=True agar output berupa key-value
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            # 3. Jalankan query SQL otomatisasi untuk menghitung total debit & kredit per akun
            cursor.execute("""
                SELECT 
                    a.id AS id,
                    a.kode_akun AS kode_akun, 
                    a.nama_akun AS nama_akun,
                    SUM(IFNULL(jd.debit, 0)) AS debit,
                    SUM(IFNULL(jd.kredit, 0)) AS kredit
                FROM akun a
                LEFT JOIN jurnal_detail jd ON a.id = jd.akun_id
                LEFT JOIN jurnal j ON jd.jurnal_id = j.id
                WHERE (j.tanggal BETWEEN %s AND %s) OR j.id IS NULL
                GROUP BY a.id, a.kode_akun, a.nama_akun
                ORDER BY a.kode_akun ASC
            """, (tanggal_awal, tanggal_akhir))
            
            data = cursor.fetchall()

            # 4. Konversi tipe data DECIMAL dari MySQL ke float agar bisa di-serialize ke JSON
            for row in data:
                row["debit"] = float(row["debit"]) if row["debit"] else 0.0
                row["kredit"] = float(row["kredit"]) if row["kredit"] else 0.0

            # 5. Bungkus data ke dalam envelope key 'data' agar cocok dengan `response.data?.data` di FE Anda
            resp.media = {"data": data}
            resp.status = falcon.HTTP_200

        except Exception as e:
            # Kirim error internal jika terjadi kesalahan query atau database
            raise falcon.HTTPInternalServerError(
                title="Database Error",
                description=str(e)
            )
            
        finally:
            # Pastikan cursor dan koneksi selalu ditutup
            cursor.close()
            conn.close()