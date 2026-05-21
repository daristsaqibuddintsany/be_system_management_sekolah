import falcon
from models.connection import get_connection


class TarifPembayaranResource:

    # =========================
    # GET ALL + FILTER + PIVOT
    # =========================
    def on_get(self, req, resp):

        kelas = req.get_param("kelas")
        tahun_ajaran = req.get_param("tahun_ajaran")
        tipe_bayar = req.get_param("tipe_bayar")
        jenis_bayar = req.get_param("jenis_bayar")
        search = req.get_param("search")

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT
            tp.id,
            tp.siswa_id,
            tp.nis,
            tp.nama_siswa,
            tp.kelas,
            tp.tahun_ajaran,
            tp.tipe_bayar,
            tp.jenis_bayar,
            tp.bulan,
            tp.nominal
        FROM tarif_pembayaran tp
        WHERE 1=1
        """

        values = []

        # =========================
        # FILTER
        # =========================

        if kelas:
            query += " AND tp.kelas=%s "
            values.append(kelas)

        if tahun_ajaran:
            query += " AND tp.tahun_ajaran=%s "
            values.append(tahun_ajaran)

        if tipe_bayar:
            query += " AND tp.tipe_bayar=%s "
            values.append(tipe_bayar)

        if jenis_bayar:
            query += " AND tp.jenis_bayar=%s "
            values.append(jenis_bayar)

        if search:
            query += """
            AND (
                tp.nama_siswa LIKE %s
                OR tp.nis LIKE %s
            )
            """
            values.append(f"%{search}%")
            values.append(f"%{search}%")

        query += """
        ORDER BY tp.nama_siswa ASC
        """

        cursor.execute(query, tuple(values))

        rows = cursor.fetchall()

        # =========================
        # PIVOT BULAN
        # =========================

        result_map = {}

        bulan_urut = [
            "Jan", "Feb", "Mar", "Apr",
            "Mei", "Jun", "Jul", "Ags",
            "Sep", "Okt", "Nov", "Des"
        ]

        for row in rows:

            key = row["nis"]

            if key not in result_map:

                result_map[key] = {
                    "id": row["id"],
                    "siswa_id": row["siswa_id"],
                    "nis": row["nis"],
                    "nama": row["nama_siswa"],
                    "kelas": row["kelas"],
                    "tahun_ajaran": row["tahun_ajaran"],
                    "tipe_bayar": row["tipe_bayar"],
                    "jenis_bayar": row["jenis_bayar"],
                    "bulan": [0] * 12
                }

            if row["bulan"] in bulan_urut:

                index_bulan = bulan_urut.index(
                    row["bulan"]
                )

                result_map[key]["bulan"][index_bulan] = (
                    row["nominal"]
                )

        cursor.close()
        conn.close()

        resp.media = {
            "data": list(result_map.values())
        }

        resp.status = falcon.HTTP_200

    # =========================
    # CREATE BULK
    # =========================
    def on_post(self, req, resp):

        body = req.media

        conn = get_connection()
        cursor = conn.cursor()

        bulan_list = [
            "Jan", "Feb", "Mar", "Apr",
            "Mei", "Jun", "Jul", "Ags",
            "Sep", "Okt", "Nov", "Des"
        ]

        for item in body:

            for i in range(12):

                cursor.execute("""
                INSERT INTO tarif_pembayaran (

                    siswa_id,
                    nis,
                    nama_siswa,
                    kelas,
                    tahun_ajaran,
                    tipe_bayar,
                    jenis_bayar,
                    bulan,
                    nominal

                )
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """, (

                    item.get("siswa_id"),
                    item.get("nis"),
                    item.get("nama_siswa"),
                    item.get("kelas"),
                    item.get("tahun_ajaran"),
                    item.get("tipe_bayar"),
                    item.get("jenis_bayar"),
                    bulan_list[i],
                    item.get("bulan")[i]

                ))

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message": "Tarif pembayaran berhasil disimpan"
        }

        resp.status = falcon.HTTP_201


class TarifPembayaranByIdResource:

    # =========================
    # UPDATE
    # =========================
    def on_put(self, req, resp, id):

        body = req.media

        bulan = body.get("bulan", [])

        conn = get_connection()
        cursor = conn.cursor()

        bulan_list = [
            "Jan", "Feb", "Mar", "Apr",
            "Mei", "Jun", "Jul", "Ags",
            "Sep", "Okt", "Nov", "Des"
        ]

        for i in range(12):

            cursor.execute("""
            UPDATE tarif_pembayaran
            SET nominal=%s
            WHERE nis=%s
            AND bulan=%s
            """, (

                bulan[i],
                id,
                bulan_list[i]

            ))

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message": "Tarif berhasil diupdate"
        }

        resp.status = falcon.HTTP_200

    # =========================
    # DELETE
    # =========================
    def on_delete(self, req, resp, id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        DELETE FROM tarif_pembayaran
        WHERE nis=%s
        """, (id,))

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message": "Data tarif berhasil dihapus"
        }

        resp.status = falcon.HTTP_200


class TarifPembayaranFilterResource:

    # =========================
    # GET FILTER
    # =========================
    def on_get(self, req, resp):

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # KELAS
        cursor.execute("""
        SELECT DISTINCT kelas
        FROM tarif_pembayaran
        ORDER BY kelas ASC
        """)

        kelas = [
            item["kelas"]
            for item in cursor.fetchall()
            if item["kelas"]
        ]

        # TAHUN AJARAN
        cursor.execute("""
        SELECT DISTINCT tahun_ajaran
        FROM tarif_pembayaran
        ORDER BY tahun_ajaran DESC
        """)

        tahun_ajaran = [
            item["tahun_ajaran"]
            for item in cursor.fetchall()
            if item["tahun_ajaran"]
        ]

        # TIPE BAYAR
        cursor.execute("""
        SELECT DISTINCT tipe_bayar
        FROM tarif_pembayaran
        ORDER BY tipe_bayar ASC
        """)

        tipe_bayar = [
            item["tipe_bayar"]
            for item in cursor.fetchall()
            if item["tipe_bayar"]
        ]

        # JENIS BAYAR
        cursor.execute("""
        SELECT DISTINCT jenis_bayar
        FROM tarif_pembayaran
        ORDER BY jenis_bayar ASC
        """)

        jenis_bayar = [
            item["jenis_bayar"]
            for item in cursor.fetchall()
            if item["jenis_bayar"]
        ]

        cursor.close()
        conn.close()

        resp.media = {
            "kelas": kelas,
            "tahun_ajaran": tahun_ajaran,
            "tipe_bayar": tipe_bayar,
            "jenis_bayar": jenis_bayar
        }

        resp.status = falcon.HTTP_200