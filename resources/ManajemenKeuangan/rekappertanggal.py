import falcon
from models.connection import get_connection


class RekapPerTanggalResource:

    # =========================================
    # GET REKAP
    # =========================================
    def on_get(self, req, resp):

        tanggal_awal = req.get_param("tanggal_awal")
        tanggal_akhir = req.get_param("tanggal_akhir")
        petugas = req.get_param("petugas")

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT

            id,

            tanggal AS tanggal,

            no_kwitansi AS noKw,

            nis,

            nama AS nama,

            kelas,

            petugas,

            nominal

        FROM rekap_per_tanggal

        WHERE 1=1
        """

        values = []

        # FILTER TANGGAL AWAL
        if tanggal_awal:

            query += """
            AND tanggal >= %s
            """

            values.append(tanggal_awal)

        # FILTER TANGGAL AKHIR
        if tanggal_akhir:

            query += """
            AND tanggal <= %s
            """

            values.append(tanggal_akhir)

        # FILTER PETUGAS
        if petugas:

            query += """
            AND petugas = %s
            """

            values.append(petugas)

        query += """
        ORDER BY tanggal DESC
        """

        cursor.execute(query, tuple(values))

        data = cursor.fetchall()

        # SUMMARY
        total_transaksi = len(data)

        total_nominal = sum(
            item["nominal"] or 0
            for item in data
        )

        result = {
            "summary": {
                "total_transaksi": total_transaksi,
                "total_nominal": total_nominal
            },
            "data": data
        }

        cursor.close()
        conn.close()

        resp.media = result
        resp.status = falcon.HTTP_200

    # =========================================
    # POST
    # =========================================
    def on_post(self, req, resp):

        body = req.media

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO rekap_per_tanggal (

            tanggal,
            no_kwitansi,
            nis,
            nama,
            kelas,
            petugas,
            nominal

        )
        VALUES (%s,%s,%s,%s,%s,%s,%s)
        """, (

            body.get("tanggal"),
            body.get("noKw"),
            body.get("nis"),
            body.get("nama"),
            body.get("kelas"),
            body.get("petugas"),
            body.get("nominal")

        ))

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message": "Data berhasil ditambahkan"
        }

        resp.status = falcon.HTTP_201


class RekapPerTanggalByIdResource:

    # =========================================
    # PUT
    # =========================================
    def on_put(self, req, resp, id):

        body = req.media

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE rekap_per_tanggal
        SET

            tanggal=%s,
            no_kwitansi=%s,
            nis=%s,
            nama=%s,
            kelas=%s,
            petugas=%s,
            nominal=%s

        WHERE id=%s
        """, (

            body.get("tanggal"),
            body.get("noKw"),
            body.get("nis"),
            body.get("nama"),
            body.get("kelas"),
            body.get("petugas"),
            body.get("nominal"),

            id

        ))

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message": "Data berhasil diupdate"
        }

        resp.status = falcon.HTTP_200

    # =========================================
    # DELETE
    # =========================================
    def on_delete(self, req, resp, id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        DELETE FROM rekap_per_tanggal
        WHERE id=%s
        """, (id,))

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message": "Data berhasil dihapus"
        }

        resp.status = falcon.HTTP_200