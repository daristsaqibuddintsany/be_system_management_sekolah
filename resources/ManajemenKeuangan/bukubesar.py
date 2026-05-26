import falcon
from datetime import datetime
from models.connection import get_connection

class BukuBesarRingkasanResource:

    # ==========================================
    # GET BUKU BESAR RINGKASAN (By Periode)
    # ==========================================
    def on_get(self, req, resp):
        # 1. Ambil filter query parameter dari React Frontend
        tanggal_awal = req.get_param('tanggal_awal')
        tanggal_akhir = req.get_param('tanggal_akhir')

        # Fallback jika Frontend tidak mengirimkan parameter tanggal
        if not tanggal_awal or not tanggal_akhir:
            today = datetime.now()
            tanggal_awal = today.replace(day=1).strftime('%Y-%m-%d')
            tanggal_akhir = today.strftime('%Y-%m-%d')

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # 2. Query agregasi data Jurnal berdasarkan Akun
        # Menghitung total debit, kredit, dan saldo akhir per akun
        query = """
            SELECT 
                a.id AS id,
                a.kode_akun AS kode, 
                a.nama_akun AS nama,
                SUM(IFNULL(jd.debit, 0)) AS debit,
                SUM(IFNULL(jd.kredit, 0)) AS kredit,
                (SUM(IFNULL(jd.debit, 0)) - SUM(IFNULL(jd.kredit, 0))) AS saldo
            FROM akun a
            LEFT JOIN jurnal_detail jd ON a.id = jd.akun_id
            LEFT JOIN jurnal j ON jd.jurnal_id = j.id
            WHERE j.tanggal BETWEEN %s AND %s OR j.id IS NULL
            GROUP BY a.id, a.kode_akun, a.nama_akun
            ORDER BY a.kode_akun ASC
        """

        try:
            cursor.execute(query, (tanggal_awal, tanggal_akhir))
            result = cursor.fetchall()

            # 3. Konversi tipe data DECIMAL/Numeric agar aman di-serialize ke JSON float
            formatted_data = []
            for row in result:
                # Jika akun belum memiliki transaksi pada periode tersebut, set ke 0
                formatted_data.append({
                    "id": row["id"],
                    "kode": row["kode"],
                    "nama": row["nama"],
                    "debit": float(row["debit"]) if row["debit"] else 0.0,
                    "kredit": float(row["kredit"]) if row["kredit"] else 0.0,
                    "saldo": float(row["saldo"]) if row["saldo"] else 0.0
                })

            # 4. Bungkus ke format envelope JSON {"data": [...]} sesuai handle React Anda (response.data.data)
            resp.media = {
                "status": "success",
                "data": formatted_data
            }
            resp.status = falcon.HTTP_200

        except Exception as e:
            raise falcon.HTTPBadRequest(
                title="Database Error", 
                description=str(e)
            )
        finally:
            cursor.close()
            conn.close()