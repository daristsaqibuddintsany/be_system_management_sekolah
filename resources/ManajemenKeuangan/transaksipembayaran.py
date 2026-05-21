import falcon
from models.connection import get_connection


class TransaksiPembayaranResource:

    # =========================
    # GET ALL TRANSAKSI
    # =========================
    def on_get(self, req, resp):

        tahun = req.get_param("tahun")
        bulan = req.get_param("bulan")
        hari_ini = req.get_param_as_bool("hari_ini") or False

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT
            p.id,

            CONCAT(
                'KW',
                LPAD(p.id, 4, '0')
            ) AS noKw,

            DATE_FORMAT(
                p.tanggal_bayar,
                '%%Y-%%m-%%d'
            ) AS tanggal,

            p.nis,

            p.nama_siswa AS nama,

            p.bulan,

            p.tahun_ajaran AS tahun,

            p.status,

            p.jumlah_bayar AS nominal

        FROM pembayaran p

        WHERE 1=1
        """

        values = []

        # FILTER TAHUN
        if tahun:
            query += " AND p.tahun_ajaran=%s "
            values.append(tahun)

        # FILTER BULAN
        if bulan:
            query += " AND p.bulan=%s "
            values.append(bulan)

        # FILTER HARI INI
        if hari_ini:
            query += """
            AND DATE(p.tanggal_bayar)=CURDATE()
            """

        query += """
        ORDER BY p.id DESC
        """

        cursor.execute(query, tuple(values))

        data = cursor.fetchall()

        # =========================
        # SUMMARY
        # =========================

        total_nominal = sum(
            item["nominal"] or 0
            for item in data
        )

        total_terbayar = len([
            item for item in data
            if item["status"] in [
                "lunas",
                "cicil",
                "aktif"
            ]
        ])

        persen = 0

        if len(data) > 0:

            persen = round(
                (total_terbayar / len(data)) * 100
            )

        cursor.close()
        conn.close()

        resp.media = {
            "summary": {
                "total_kwitansi": len(data),
                "total_nominal": total_nominal,
                "persen_terbayar": persen
            },

            "data": data
        }

        resp.status = falcon.HTTP_200

    # =========================
    # CREATE TRANSAKSI
    # =========================
    def on_post(self, req, resp):

        body = req.media

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO pembayaran (

            tanggal_bayar,
            nis,
            nama_siswa,
            bulan,
            tahun_ajaran,
            jumlah_bayar,
            status

        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (

            body.get("tanggal"),
            body.get("nis"),
            body.get("nama"),
            body.get("bulan"),
            body.get("tahun"),
            body.get("nominal"),
            body.get("status")

        ))

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message": "Transaksi berhasil ditambahkan"
        }

        resp.status = falcon.HTTP_201


class TransaksiPembayaranByIdResource:

    # =========================
    # DETAIL
    # =========================
    def on_get(self, req, resp, id):

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
        SELECT

            p.id,

            CONCAT(
                'KW',
                LPAD(p.id, 4, '0')
            ) AS noKw,

            DATE_FORMAT(
                p.tanggal_bayar,
                '%%Y-%%m-%%d'
            ) AS tanggal,

            p.nis,

            p.nama_siswa AS nama,

            p.bulan,

            p.tahun_ajaran AS tahun,

            p.status,

            p.jumlah_bayar AS nominal

        FROM pembayaran p

        WHERE p.id=%s
        """, (id,))

        data = cursor.fetchone()

        cursor.close()
        conn.close()

        if not data:

            resp.media = {
                "message": "Data tidak ditemukan"
            }

            resp.status = falcon.HTTP_404
            return

        resp.media = data
        resp.status = falcon.HTTP_200

    # =========================
    # UPDATE
    # =========================
    def on_put(self, req, resp, id):

        body = req.media

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE pembayaran
        SET

            nis=%s,
            nama_siswa=%s,
            bulan=%s,
            tahun_ajaran=%s,
            status=%s,
            jumlah_bayar=%s

        WHERE id=%s
        """, (

            body.get("nis"),
            body.get("nama"),
            body.get("bulan"),
            body.get("tahun"),
            body.get("status"),
            body.get("nominal"),
            id

        ))

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message": "Transaksi berhasil diupdate"
        }

        resp.status = falcon.HTTP_200

    # =========================
    # DELETE
    # =========================
    def on_delete(self, req, resp, id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        DELETE FROM pembayaran
        WHERE id=%s
        """, (id,))

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message": "Transaksi berhasil dihapus"
        }

        resp.status = falcon.HTTP_200


class PrintTransaksiPembayaranResource:

    # =========================
    # PRINT DATA
    # =========================
    def on_get(self, req, resp, id):

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
        SELECT

            p.id,

            CONCAT(
                'KW',
                LPAD(p.id, 4, '0')
            ) AS noKw,

            DATE_FORMAT(
                p.tanggal_bayar,
                '%%Y-%%m-%%d'
            ) AS tanggal,

            p.nis,

            p.nama_siswa AS nama,

            p.kelas,

            p.bulan,

            p.tahun_ajaran AS tahun,

            p.status,

            p.jumlah_bayar AS nominal

        FROM pembayaran p

        WHERE p.id=%s
        """, (id,))

        data = cursor.fetchone()

        cursor.close()
        conn.close()

        if not data:

            resp.media = {
                "message": "Data tidak ditemukan"
            }

            resp.status = falcon.HTTP_404
            return

        resp.media = {
            "message": "Print transaksi berhasil",
            "data": data
        }

        resp.status = falcon.HTTP_200