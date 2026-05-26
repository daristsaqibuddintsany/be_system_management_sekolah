import falcon
from datetime import datetime
from models.connection import get_connection

class PenghasilanKomprehensifResource:

    # ==========================================
    # GET DATA LAPORAN PENGHASILAN KOMPREHENSIF
    # ==========================================
    def on_get(self, req, resp):
        # 1. Ambil parameter filter tanggal dari query string Axios
        tanggal_awal = req.get_param('tanggal_awal')
        tanggal_akhir = req.get_param('tanggal_akhir')

        # Fallback jika parameter tanggal kosong (default bulan berjalan)
        if not tanggal_awal or not tanggal_akhir:
            today = datetime.now()
            tanggal_awal = today.replace(day=1).strftime('%Y-%m-%d')
            tanggal_akhir = today.strftime('%Y-%m-%d')

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            # 2. Jalankan query untuk memfilter laporan berdasarkan rentang tanggal
            cursor.execute("""
                SELECT 
                    nama_akun AS nama,
                    tipe,
                    dengan_pembatasan AS pembatasan,
                    tanpa_pembatasan AS tanpa
                FROM laporan_penghasilan_komprehensif
                WHERE tanggal BETWEEN %s AND %s
                ORDER BY id ASC
            """, (tanggal_awal, tanggal_akhir))
            
            rows = cursor.fetchall()

            # 3. Pisahkan data ke kategori pendapatan dan beban sesuai struktur FE
            list_pendapatan = []
            list_beban = []

            for row in rows:
                # Konversi nilai numerik ke float/int agar aman di JSON
                item = {
                    "nama": row["nama"],
                    "pembatasan": float(row["pembatasan"]),
                    "tanpa": float(row["tanpa"])
                }
                
                if row["tipe"] == 'Pendapatan':
                    list_pendapatan.append(item)
                elif row["tipe"] == 'Beban':
                    list_beban.append(item)

            # 4. Satukan respon ke format objek yang siap di-destructure oleh Frontend
            resp.media = {
                "pendapatan": list_pendapatan,
                "beban": list_beban
            }
            resp.status = falcon.HTTP_200

        except Exception as e:
            raise falcon.HTTPInternalServerError(
                title="Database Error",
                description=str(e)
            )
            
        finally:
            cursor.close()
            conn.close()