import falcon
from datetime import datetime
from models.connection import get_connection

class PosisiKeuanganResource:

    # ==========================================
    # GET DATA LAPORAN POSISI KEUANGAN (NERACA)
    # ==========================================
    def on_get(self, req, resp):
        # 1. Ambil parameter filter tanggal awal dan akhir dari query string Axios
        tanggal_awal = req.get_param('tanggal_awal')
        tanggal_akhir = req.get_param('tanggal_akhir')

        # Fallback jika parameter tanggal dikirim kosong (default bulan berjalan)
        if not tanggal_awal or not tanggal_akhir:
            today = datetime.now()
            tanggal_awal = today.replace(day=1).strftime('%Y-%m-%d')
            tanggal_akhir = today.strftime('%Y-%m-%d')

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            # 2. Jalankan query mengambil item posisi keuangan berdasarkan rentang tanggal
            cursor.execute("""
                SELECT 
                    nama_akun AS nama,
                    kategori,
                    nominal
                FROM laporan_posisi_keuangan
                WHERE tanggal BETWEEN %s AND %s
                ORDER BY id ASC
            """, (tanggal_awal, tanggal_akhir))
            
            rows = cursor.fetchall()

            # 3. Pisahkan data ke kategori aset dan liabilitas sesuai kebutuhan React
            list_aset = []
            list_liabilitas = []

            for row in rows:
                item = {
                    "nama": row["nama"],
                    "nominal": float(row["nominal"]) if row["nominal"] else 0.0
                }
                
                if row["kategori"] == 'Aset':
                    list_aset.append(item)
                elif row["kategori"] == 'Liabilitas':
                    list_liabilitas.append(item)

            # 4. Ambil data Laba Tahun Berjalan (diambil dari selisih pendapatan & beban periode terkait)
            # Query ini mengasumsikan Anda mengambil nilai bersih laba rugi dari tabel komprehensif sebelumnya
            cursor.execute("""
                SELECT 
                    SUM(IF(tipe = 'Pendapatan', dengan_pembatasan + tanpa_pembatasan, 0)) -
                    SUM(IF(tipe = 'Beban', dengan_pembatasan + tanpa_pembatasan, 0)) AS laba_bersih
                FROM laporan_penghasilan_komprehensif
                WHERE tanggal BETWEEN %s AND %s
            """, (tanggal_awal, tanggal_akhir))
            
            result_laba = cursor.fetchone()
            laba_tahun_berjalan = float(result_laba["laba_bersih"]) if result_laba and result_laba["laba_bersih"] else 0.0

            # 5. Bungkus semua data ke dalam JSON response
            resp.media = {
                "aset": list_aset,
                "liabilitas": list_liabilitas,
                "laba": laba_tahun_berjalan
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