# =====================================================
# resources/ManajemenKeuangan/realisasianggaran.py
# =====================================================

import falcon
from models.connection import get_connection


class RealisasiAnggaranResource:

    # =========================================
    # GET ALL
    # =========================================
    def on_get(self, req, resp):

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
        SELECT *
        FROM realisasi_anggaran
        ORDER BY id DESC
        """)

        data = cursor.fetchall()

        cursor.close()
        conn.close()

        resp.media = data


    # =========================================
    # INSERT
    # =========================================
    def on_post(self, req, resp):

        body = req.media

        conn = get_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO realisasi_anggaran (
            kode_akun,
            nama_akun,
            kategori,
            tahun_ajaran,
            pagu,

            juli,
            agustus,
            september,
            oktober,
            november,
            desember,
            januari,
            februari,
            maret,
            april,
            mei,
            juni
        )
        VALUES (
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s
        )
        """

        values = (
            body["kode_akun"],
            body["nama_akun"],
            body["kategori"],
            body["tahun_ajaran"],
            body.get("pagu", 0),

            body.get("juli", 0),
            body.get("agustus", 0),
            body.get("september", 0),
            body.get("oktober", 0),
            body.get("november", 0),
            body.get("desember", 0),
            body.get("januari", 0),
            body.get("februari", 0),
            body.get("maret", 0),
            body.get("april", 0),
            body.get("mei", 0),
            body.get("juni", 0),
        )

        cursor.execute(query, values)

        conn.commit()

        resp.status = falcon.HTTP_201
        resp.media = {
            "message": "Data realisasi anggaran berhasil ditambahkan"
        }

        cursor.close()
        conn.close()


class RealisasiAnggaranByIdResource:

    # =========================================
    # GET BY ID
    # =========================================
    def on_get(self, req, resp, id):

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
        SELECT *
        FROM realisasi_anggaran
        WHERE id = %s
        """, (id,))

        data = cursor.fetchone()

        cursor.close()
        conn.close()

        if not data:
            resp.status = falcon.HTTP_404
            resp.media = {
                "message": "Data tidak ditemukan"
            }
            return

        resp.media = data


    # =========================================
    # UPDATE
    # =========================================
    def on_put(self, req, resp, id):

        body = req.media

        conn = get_connection()
        cursor = conn.cursor()

        query = """
        UPDATE realisasi_anggaran
        SET
            kode_akun = %s,
            nama_akun = %s,
            kategori = %s,
            tahun_ajaran = %s,
            pagu = %s,

            juli = %s,
            agustus = %s,
            september = %s,
            oktober = %s,
            november = %s,
            desember = %s,
            januari = %s,
            februari = %s,
            maret = %s,
            april = %s,
            mei = %s,
            juni = %s

        WHERE id = %s
        """

        values = (
            body["kode_akun"],
            body["nama_akun"],
            body["kategori"],
            body["tahun_ajaran"],
            body.get("pagu", 0),

            body.get("juli", 0),
            body.get("agustus", 0),
            body.get("september", 0),
            body.get("oktober", 0),
            body.get("november", 0),
            body.get("desember", 0),
            body.get("januari", 0),
            body.get("februari", 0),
            body.get("maret", 0),
            body.get("april", 0),
            body.get("mei", 0),
            body.get("juni", 0),

            id
        )

        cursor.execute(query, values)

        conn.commit()

        resp.media = {
            "message": "Data realisasi anggaran berhasil diupdate"
        }

        cursor.close()
        conn.close()


    # =========================================
    # DELETE
    # =========================================
    def on_delete(self, req, resp, id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        DELETE FROM realisasi_anggaran
        WHERE id = %s
        """, (id,))

        conn.commit()

        resp.media = {
            "message": "Data realisasi anggaran berhasil dihapus"
        }

        cursor.close()
        conn.close()