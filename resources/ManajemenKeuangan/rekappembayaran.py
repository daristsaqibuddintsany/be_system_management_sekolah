import falcon
from models.connection import get_connection


class RekapPembayaranResource:

    # ======================================
    # GET DATA REKAP
    # ======================================
    def on_get(self, req, resp):

        kelas = req.get_param("kelas")
        tahun = req.get_param("tahun_ajaran")
        tipe = req.get_param("tipe_bayar")
        jenis = req.get_param("jenis_bayar")

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT *
        FROM rekap_pembayaran
        WHERE 1=1
        """

        params = []

        # FILTER
        if kelas:
            query += " AND kelas = %s"
            params.append(kelas)

        if tahun:
            query += " AND tahun = %s"
            params.append(tahun)

        if tipe:
            query += " AND tipe = %s"
            params.append(tipe)

        if jenis:
            query += " AND jenis = %s"
            params.append(jenis)

        query += " ORDER BY id DESC"

        cursor.execute(query, params)

        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        resp.media = {
            "data": rows
        }

        resp.status = falcon.HTTP_200

    # ======================================
    # CREATE
    # ======================================
    def on_post(self, req, resp):

        body = req.media

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO rekap_pembayaran (

            nis,
            nama,
            kelas,
            tahun,
            tipe,
            jenis,

            jan,
            feb,
            mar,
            apr,
            mei,
            jun,
            jul,
            ags,
            sep,
            okt,
            nov,
            des

        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (

            body.get("nis"),
            body.get("nama"),
            body.get("kelas", ""),
            body.get("tahun"),
            body.get("tipe", ""),
            body.get("jenis"),

            body.get("jan", "✖"),
            body.get("feb", "✖"),
            body.get("mar", "✖"),
            body.get("apr", "✖"),
            body.get("mei", "✖"),
            body.get("jun", "✖"),
            body.get("jul", "✖"),
            body.get("ags", "✖"),
            body.get("sep", "✖"),
            body.get("okt", "✖"),
            body.get("nov", "✖"),
            body.get("des", "✖")

        ))

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message": "Data berhasil ditambahkan"
        }

        resp.status = falcon.HTTP_201


class RekapPembayaranByIdResource:

    # ======================================
    # UPDATE
    # ======================================
    def on_put(self, req, resp, id):

        body = req.media

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE rekap_pembayaran
        SET

            nis=%s,
            nama=%s,
            tahun=%s,
            jenis=%s,

            jan=%s,
            feb=%s,
            mar=%s,
            apr=%s,
            mei=%s,
            jun=%s,
            jul=%s,
            ags=%s,
            sep=%s,
            okt=%s,
            nov=%s,
            des=%s

        WHERE id=%s
        """, (

            body.get("nis"),
            body.get("nama"),
            body.get("tahun"),
            body.get("jenis"),

            body.get("jan"),
            body.get("feb"),
            body.get("mar"),
            body.get("apr"),
            body.get("mei"),
            body.get("jun"),
            body.get("jul"),
            body.get("ags"),
            body.get("sep"),
            body.get("okt"),
            body.get("nov"),
            body.get("des"),

            id

        ))

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message": "Data berhasil diupdate"
        }

        resp.status = falcon.HTTP_200

    # ======================================
    # DELETE
    # ======================================
    def on_delete(self, req, resp, id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        DELETE FROM rekap_pembayaran
        WHERE id = %s
        """, (id,))

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message": "Data berhasil dihapus"
        }

        resp.status = falcon.HTTP_200


class RekapPembayaranFilterResource:

    # ======================================
    # GET FILTER OPTION
    # ======================================
    def on_get(self, req, resp):

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # KELAS
        cursor.execute("""
        SELECT DISTINCT kelas
        FROM rekap_pembayaran
        ORDER BY kelas ASC
        """)

        kelas = [
            row["kelas"]
            for row in cursor.fetchall()
            if row["kelas"]
        ]

        # TAHUN
        cursor.execute("""
        SELECT DISTINCT tahun
        FROM rekap_pembayaran
        ORDER BY tahun ASC
        """)

        tahun = [
            row["tahun"]
            for row in cursor.fetchall()
            if row["tahun"]
        ]

        # TIPE
        cursor.execute("""
        SELECT DISTINCT tipe
        FROM rekap_pembayaran
        ORDER BY tipe ASC
        """)

        tipe = [
            row["tipe"]
            for row in cursor.fetchall()
            if row["tipe"]
        ]

        # JENIS
        cursor.execute("""
        SELECT DISTINCT jenis
        FROM rekap_pembayaran
        ORDER BY jenis ASC
        """)

        jenis = [
            row["jenis"]
            for row in cursor.fetchall()
            if row["jenis"]
        ]

        cursor.close()
        conn.close()

        resp.media = {
            "kelas": kelas,
            "tahun": tahun,
            "tipe": tipe,
            "jenis": jenis
        }

        resp.status = falcon.HTTP_200