import falcon
from datetime import datetime
from models.connection import get_connection


class TransaksiTabunganTellerResource:

    # =========================
    # GET ALL
    # =========================
    def on_get(self, req, resp):

        search = req.get_param("search")
        jenis = req.get_param("jenis")

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT
            id,
            nis,
            jenis,
            nominal,
            keterangan,
            created_at
        FROM transaksi_tabungan_teller
        WHERE 1=1
        """

        values = []

        # FILTER SEARCH
        if search:

            query += """
            AND (
                nis LIKE %s
            )
            """

            values.append(f"%{search}%")

        # FILTER JENIS
        if jenis:

            query += """
            AND jenis=%s
            """

            values.append(jenis)

        query += """
        ORDER BY created_at DESC
        """

        cursor.execute(query, tuple(values))

        data = cursor.fetchall()

        cursor.close()
        conn.close()

        resp.media = {
            "data": data
        }

        resp.status = falcon.HTTP_200

    # =========================
    # POST
    # =========================
    def on_post(self, req, resp):

        body = req.media

        nis = body.get("nis")
        jenis = body.get("jenis")
        nominal = body.get("nominal")
        keterangan = body.get("keterangan")

        if not nis or not nominal:

            resp.media = {
                "message": "NIS dan nominal wajib diisi"
            }

            resp.status = falcon.HTTP_400
            return

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO transaksi_tabungan_teller (

            nis,
            jenis,
            nominal,
            keterangan

        )
        VALUES (%s,%s,%s,%s)
        """, (

            nis,
            jenis,
            nominal,
            keterangan

        ))

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message": "Transaksi berhasil disimpan"
        }

        resp.status = falcon.HTTP_201


class TransaksiTabunganTellerByIdResource:

    # =========================
    # PUT
    # =========================
    def on_put(self, req, resp, id):

        body = req.media

        nis = body.get("nis")
        jenis = body.get("jenis")
        nominal = body.get("nominal")
        keterangan = body.get("keterangan")

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE transaksi_tabungan_teller
        SET

            nis=%s,
            jenis=%s,
            nominal=%s,
            keterangan=%s

        WHERE id=%s
        """, (

            nis,
            jenis,
            nominal,
            keterangan,
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
        DELETE FROM transaksi_tabungan_teller
        WHERE id=%s
        """, (id,))

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message": "Transaksi berhasil dihapus"
        }

        resp.status = falcon.HTTP_200