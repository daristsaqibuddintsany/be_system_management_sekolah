import falcon
from datetime import datetime
from models.connection import get_connection

class PerubahanAsetNetoResource:

    # ==========================================
    # GET DATA LAPORAN PERUBAHAN ASET NETO
    # ==========================================
    def on_get(self, req, resp):
        # 1. Ambil parameter filter dari query string Axios Frontend
        tanggal_awal = req.get_param('tanggal_awal')
        tanggal_akhir = req.get_param('tanggal_akhir')

        # Fallback default tanggal jika parameter kosong
        if not tanggal_awal or not tanggal_akhir:
            today = datetime.now()
            tanggal_awal = today.replace(day=1).strftime('%Y-%m-%d')
            tanggal_akhir = today.strftime('%Y-%m-%d')

        # Parsing tahun untuk mencari saldo awal historis
        try:
            tahun_berjalan = datetime.strptime(tanggal_akhir, '%Y-%m-%d').year
            tahun_lalu = tahun_berjalan - 1
        except Exception:
            tahun_berjalan = 2026
            tahun_lalu = 2025

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            # 2. Ambil data Saldo Awal historis dari tabel perubahan aset neto (Tahun Lalu)
            cursor.execute("""
                SELECT 
                    IFNULL(aset_neto_dengan_pembatasan, 0) AS awal_pembatasan,
                    IFNULL(aset_neto_tanpa_pembatasan, 0) AS awal_tanpa
                FROM laporan_perubahan_aset_neto
                WHERE tahun = %s
                LIMIT 1
            """, (tahun_lalu,))
            
            saldo_historis = cursor.fetchone()
            
            # Jika data tahun lalu belum ada di database, set default ke 0
            if not saldo_historis:
                saldo_historis = {"awal_pembatasan": 0.0, "awal_tanpa": 0.0}

            # 3. Ambil data Surplus/Defisit Berjalan dari tabel laporan komprehensif
            cursor.execute("""
                SELECT 
                    SUM(IF(tipe = 'Pendapatan', dengan_pembatasan, 0)) - 
                    SUM(IF(tipe = 'Beban', dengan_pembatasan, 0)) AS surplus_dengan_pembatasan,
                    
                    SUM(IF(tipe = 'Pendapatan', tanpa_pembatasan, 0)) - 
                    SUM(IF(tipe = 'Beban', tanpa_pembatasan, 0)) AS surplus_tanpa_pembatasan
                FROM laporan_penghasilan_komprehensif
                WHERE tanggal BETWEEN %s AND %s
            """, (tanggal_awal, tanggal_akhir))
            
            surplus_data = cursor.fetchone()
            
            surplus_dengan = float(surplus_data["surplus_dengan_pembatasan"]) if surplus_data and surplus_data["surplus_dengan_pembatasan"] else 0.0
            surplus_tanpa = float(surplus_data["surplus_tanpa_pembatasan"]) if surplus_data and surplus_data["surplus_tanpa_pembatasan"] else 0.0

            # 4. Bungkus semua data ke format JSON untuk merestrukturisasi tabel Frontend
            resp.media = {
                "tahun_lalu": {
                    "label": f"30 Apr {tahun_lalu}",
                    "dengan_pembatasan": float(saldo_historis["awal_pembatasan"]),
                    "tanpa_pembatasan": float(saldo_historis["awal_tanpa"])
                },
                "tahun_berjalan": {
                    "label": f"30 Apr {tahun_berjalan}",
                    "surplus_dengan_pembatasan": surplus_dengan,
                    "surplus_tanpa_pembatasan": surplus_tanpa
                }
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