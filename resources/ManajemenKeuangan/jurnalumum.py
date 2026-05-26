import falcon
from datetime import datetime
from models.connection import get_connection

class JurnalUmumResource:

    # ==========================================
    # GET DATA JURNAL UMUM
    # ==========================================
    def on_get(self, req, resp):
        # 1. Ambil parameter filter dari query string Axios
        tanggal_awal = req.get_param('tanggal_awal')
        tanggal_akhir = req.get_param('tanggal_akhir')

        # Fallback jika parameter tanggal kosong
        if not tanggal_awal or not tanggal_akhir:
            today = datetime.now()
            tanggal_awal = today.replace(day=1).strftime('%Y-%m-%d')
            tanggal_akhir = today.strftime('%Y-%m-%d')

        # 2. Buka koneksi database dengan dictionary=True agar key-nya cocok dengan mapping item di React
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            # 3. Jalankan query untuk memfilter laporan jurnal umum berdasarkan rentang tanggal
            cursor.execute("""
                SELECT 
                    id,
                    DATE_FORMAT(tanggal, '%Y-%m-%d') AS tanggal,
                    kode_transaksi,
                    kode_akun,
                    nama_akun,
                    debit,
                    kredit,
                    keterangan AS ket
                FROM laporan_jurnal_umum
                WHERE tanggal BETWEEN %s AND %s
                ORDER BY tanggal ASC, id ASC
            """, (tanggal_awal, tanggal_akhir))
            
            data = cursor.fetchall()

            # 4. Konversi tipe data numerik BIGINT/DECIMAL ke float agar aman saat proses JSON serialization
            for row in data:
                row["debit"] = float(row["debit"]) if row["debit"] else 0.0
                row["kredit"] = float(row["kredit"]) if row["kredit"] else 0.0

            # 5. Berikan respon balik ke Frontend. Dibungkus key 'data' agar terbaca oleh response.data?.data
            resp.media = {"data": data}
            resp.status = falcon.HTTP_200

        except Exception as e:
            raise falcon.HTTPInternalServerError(
                title="Database Error",
                description=str(e)
            )
            
        finally:
            # Tutup koneksi agar resource database tidak bocor
            cursor.close()
            conn.close()