import falcon
from models.connection import get_connection


class AkunKeuanganResource:

    # =========================
    # GET ALL
    # =========================
    def on_get(self, req, resp):

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
        SELECT *
        FROM akun_keuangan
        ORDER BY id DESC
        """)

        data = cursor.fetchall()

        cursor.close()
        conn.close()

        resp.media = data


    # =========================
    # INSERT
    # =========================
    def on_post(self, req, resp):

        data = req.media

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO akun_keuangan (
            kode,
            nama,
            kelompok,
            golongan,
            budgeting,
            arus_kas,
            keterangan
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            data["kode"],
            data["nama"],
            data["kelompok"],
            data["golongan"],
            data.get("budgeting", ""),
            data.get("arus_kas", ""),
            data.get("keterangan", "")
        ))

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message": "Data akun keuangan berhasil ditambahkan"
        }


class AkunKeuanganByIdResource:

    # =========================
    # GET BY ID
    # =========================
    def on_get(self, req, resp, id):

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
        SELECT *
        FROM akun_keuangan
        WHERE id = %s
        """, (id,))

        data = cursor.fetchone()

        cursor.close()
        conn.close()

        resp.media = data


    # =========================
    # UPDATE
    # =========================
    def on_put(self, req, resp, id):

        data = req.media

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE akun_keuangan
        SET
            kode = %s,
            nama = %s,
            kelompok = %s,
            golongan = %s,
            budgeting = %s,
            arus_kas = %s,
            keterangan = %s
        WHERE id = %s
        """, (
            data["kode"],
            data["nama"],
            data["kelompok"],
            data["golongan"],
            data.get("budgeting", ""),
            data.get("arus_kas", ""),
            data.get("keterangan", ""),
            id
        ))

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message": "Data akun keuangan berhasil diupdate"
        }


    # =========================
    # DELETE
    # =========================
    def on_delete(self, req, resp, id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        DELETE FROM akun_keuangan
        WHERE id = %s
        """, (id,))

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message": "Data akun keuangan berhasil dihapus"
        }