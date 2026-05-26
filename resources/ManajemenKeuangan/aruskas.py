import falcon
from datetime import datetime
from models.connection import get_connection

class ArusKasResource:

    # ==========================================
    # GET DATA LAPORAN ARUS KAS
    # ==========================================
    def on_get(self, req, resp):
        # 1. Tangkap parameter tanggal dari Axios
        tanggal_awal = req.get_param('tanggal_awal')
        tanggal_akhir = req.get_param('tanggal_akhir')

        # Fallback default tanggal jika parameter kosong
        if not tanggal_awal or not tanggal_akhir:
            today = datetime.now()
            tanggal_awal = today.replace(day=1).strftime('%Y-%m-%d')
            tanggal_akhir = today.strftime('%Y-%m-%d')

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            # 2. Ambil data mutasi kas berdasarkan periode filter
            cursor.execute("""
                SELECT 
                    nama_akun AS nama,
                    aktivitas,
                    nominal
                FROM laporan_arus_kas
                WHERE tanggal BETWEEN %s AND %s
                ORDER BY id ASC
            """, (tanggal_awal, tanggal_akhir))
            
            rows = cursor.fetchall()

            # 3. Inisialisasi wadah penampung data sesuai array di React
            list_operasi = []
            list_investasi = []
            list_pendanaan = []

            for row in rows:
                item = {
                    "nama": row["nama"],
                    "nominal": float(row["nominal"]) if row["nominal"] else 0.0
                }
                
                # Pengelompokan berdasarkan nilai ENUM aktivitas
                if row["aktivitas"] == 'Operasi':
                    list_operasi.append(item)
                elif row["aktivitas"] == 'Investasi':
                    list_investasi.append(item)
                elif row["aktivitas"] == 'Pendanaan':
                    list_pendanaan.append(item)

            # 4. Kembalikan data dalam bentuk JSON terstruktur
            resp.media = {
                "operasi": list_operasi,
                "investasi": list_investasi,
                "pendanaan": list_pendanaan
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