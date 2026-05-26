# =====================================================
# resources/ManajemenKeuangan/evaluasianggaran.py
# =====================================================

import falcon
from models.connection import get_connection


class EvaluasiAnggaranResource:

    # =========================================
    # GET ALL
    # =========================================
    def on_get(self, req, resp):

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
        SELECT *
        FROM evaluasi_anggaran
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
        INSERT INTO evaluasi_anggaran (
            kode_akun,
            nama_akun,
            kelompok,
            tahun_ajaran,
            pagu,
            q1,
            q2,
            q3,
            q4,
            total_realisasi,
            sisa_surplus,
            forecast,
            persentase
        )
        VALUES (
            %s, %s, %s, %s,
            %s, %s, %s, %s,
            %s, %s, %s, %s, %s
        )
        """

        values = (
            body["kode_akun"],
            body["nama_akun"],
            body["kelompok"],
            body["tahun_ajaran"],

            body.get("pagu", 0),
            body.get("q1", 0),
            body.get("q2", 0),
            body.get("q3", 0),
            body.get("q4", 0),

            body.get("total_realisasi", 0),
            body.get("sisa_surplus", 0),
            body.get("forecast", 0),
            body.get("persentase", 0),
        )

        cursor.execute(query, values)

        conn.commit()

        resp.status = falcon.HTTP_201
        resp.media = {
            "message": "Data evaluasi anggaran berhasil ditambahkan"
        }

        cursor.close()
        conn.close()


class EvaluasiAnggaranByIdResource:

    # =========================================
    # GET BY ID
    # =========================================
    def on_get(self, req, resp, id):

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
        SELECT *
        FROM evaluasi_anggaran
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
        UPDATE evaluasi_anggaran
        SET
            kode_akun = %s,
            nama_akun = %s,
            kelompok = %s,
            tahun_ajaran = %s,
            pagu = %s,
            q1 = %s,
            q2 = %s,
            q3 = %s,
            q4 = %s,
            total_realisasi = %s,
            sisa_surplus = %s,
            forecast = %s,
            persentase = %s
        WHERE id = %s
        """

        values = (
            body["kode_akun"],
            body["nama_akun"],
            body["kelompok"],
            body["tahun_ajaran"],

            body.get("pagu", 0),
            body.get("q1", 0),
            body.get("q2", 0),
            body.get("q3", 0),
            body.get("q4", 0),

            body.get("total_realisasi", 0),
            body.get("sisa_surplus", 0),
            body.get("forecast", 0),
            body.get("persentase", 0),

            id
        )

        cursor.execute(query, values)

        conn.commit()

        resp.media = {
            "message": "Data evaluasi anggaran berhasil diupdate"
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
        DELETE FROM evaluasi_anggaran
        WHERE id = %s
        """, (id,))

        conn.commit()

        resp.media = {
            "message": "Data evaluasi anggaran berhasil dihapus"
        }

        cursor.close()
        conn.close()