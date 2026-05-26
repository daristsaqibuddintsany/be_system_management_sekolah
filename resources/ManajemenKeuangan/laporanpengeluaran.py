import falcon
from models.connection import get_connection

class LaporanPengeluaranResource:

    # ==========================================
    # GET ALL TRANSAKSI LAPORAN + FILTER TANGGAL
    # ==========================================
    def on_get(self, req, resp):
        # Mengambil query params dari axios frontend (?tanggal_awal=...&tanggal_akhir=...)
        tanggal_awal = req.get_param('tanggal_awal')
        tanggal_akhir = req.get_param('tanggal_akhir')

        # Validasi dasar jika parameter filter kosong
        if not tanggal_awal or not tanggal_akhir:
            raise falcon.HTTPBadRequest(
                title="Missing Parameters",
                description="Parameter 'tanggal_awal' dan 'tanggal_akhir' wajib disertakan."
            )

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # Query data dengan filter rentang tanggal, diurutkan dari yang terbaru
        # Kolom 'petugas' dimasukkan atau diredireksi dari admin/user pembuat jika ada relasi tabelnya
        query = """
            SELECT 
                id, 
                kode, 
                DATE_FORMAT(tanggal, '%Y-%m-%d') as tanggal, 
                jenis, 
                bidang, 
                penerima, 
                sumber, 
                'Admin' as petugas, -- Isian default/hardcode sementara, silakan ganti sesuai kolom tabelmu
                menyetujui, 
                keterangan, 
                nominal
            FROM transaksi_pengeluaran
            WHERE tanggal BETWEEN %s AND %s
            ORDER BY tanggal DESC, id DESC
        """
        
        cursor.execute(query, (tanggal_awal, tanggal_akhir))
        data = cursor.fetchall()

        # Konversi tipe data nominal ke float/int agar aman saat di-serialize ke JSON
        for row in data:
            if row["nominal"] is not None:
                row["nominal"] = int(row["nominal"])

        cursor.close()
        conn.close()

        # Set output data untuk diproses komponen React
        resp.media = data
        resp.status = falcon.HTTP_200