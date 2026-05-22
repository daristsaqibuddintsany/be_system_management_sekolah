import falcon
from datetime import datetime
from models.connection import get_connection


class TransaksiPenerimaanResource:

    # =========================
    # GET ALL
    # =========================
    def on_get(self, req, resp):

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
        SELECT

            id,
            kode,
            jenis,
            sumber,
            tanggal,
            nominal,
            menyetujui,
            keterangan

        FROM transaksi_penerimaan

        ORDER BY id DESC
        """)

        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        resp.media = rows

        resp.status = falcon.HTTP_200

    # =========================
    # POST
    # =========================
    def on_post(self, req, resp):

        body = req.media

        jenis = body.get("jenis")
        sumber = body.get("sumber")
        tanggal = body.get("tanggal")
        nominal = body.get("nominal")
        menyetujui = body.get("menyetujui")
        keterangan = body.get("keterangan")

        conn = get_connection()
        cursor = conn.cursor()

        # =========================
        # GENERATE KODE
        # =========================

        kode = (
            "TP-" +
            datetime.now().strftime("%Y%m%d%H%M%S")
        )

        # =========================
        # FORMAT TANGGAL
        # =========================

        tanggal_db = None

        try:

            if "/" in tanggal:

                tanggal_db = datetime.strptime(
                    tanggal,
                    "%d/%m/%Y"
                ).strftime("%Y-%m-%d")

            else:

                tanggal_db = tanggal

        except:
            tanggal_db = datetime.now().strftime(
                "%Y-%m-%d"
            )

        # =========================
        # INSERT
        # =========================

        cursor.execute("""
        INSERT INTO transaksi_penerimaan (

            kode,
            jenis,
            sumber,
            tanggal,
            nominal,
            menyetujui,
            keterangan

        )
        VALUES (%s,%s,%s,%s,%s,%s,%s)
        """, (

            kode,
            jenis,
            sumber,
            tanggal_db,
            nominal,
            menyetujui,
            keterangan

        ))

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message":
            "Transaksi berhasil disimpan"
        }

        resp.status = falcon.HTTP_201


class TransaksiPenerimaanByIdResource:

    # =========================
    # UPDATE
    # =========================
    def on_put(self, req, resp, id):

        body = req.media

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE transaksi_penerimaan
        SET

            jenis=%s,
            sumber=%s,
            tanggal=%s,
            nominal=%s,
            menyetujui=%s,
            keterangan=%s

        WHERE id=%s
        """, (

            body.get("jenis"),
            body.get("sumber"),
            body.get("tanggal"),
            body.get("nominal"),
            body.get("menyetujui"),
            body.get("keterangan"),
            id

        ))

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message":
            "Data berhasil diupdate"
        }

        resp.status = falcon.HTTP_200

    # =========================
    # DELETE
    # =========================
    def on_delete(self, req, resp, id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        DELETE FROM transaksi_penerimaan
        WHERE id=%s
        """, (id,))

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message":
            "Data berhasil dihapus"
        }

        resp.status = falcon.HTTP_200