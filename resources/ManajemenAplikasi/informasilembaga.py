import falcon
from models.connection import get_connection


class InformasiLembagaResource:

    # =========================
    # GET ALL / SEARCH
    # =========================
    def on_get(self, req, resp):

        search = req.get_param("search")

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT *
        FROM informasi_lembaga
        WHERE 1=1
        """

        values = []

        if search:
            query += " AND (judul LIKE %s OR isi LIKE %s)"
            values.extend([f"%{search}%", f"%{search}%"])

        query += " ORDER BY id DESC"

        cursor.execute(query, tuple(values))
        data = cursor.fetchall()

        cursor.close()
        conn.close()

        resp.media = data

    # =========================
    # INSERT DATA
    # =========================
    def on_post(self, req, resp):

        data = req.media

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO informasi_lembaga (
            judul,
            isi,
            tanggal
        ) VALUES (%s, %s, %s)
        """, (
            data["judul"],
            data["isi"],
            data["tanggal"]
        ))

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message": "Informasi berhasil ditambahkan"
        }

    # =========================
    # UPDATE DATA
    # =========================
    def on_put(self, req, resp, id):

        data = req.media

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE informasi_lembaga
        SET judul = %s,
            isi = %s,
            tanggal = %s
        WHERE id = %s
        """, (
            data["judul"],
            data["isi"],
            data["tanggal"],
            id
        ))

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message": "Informasi berhasil diupdate"
        }

    # =========================
    # DELETE DATA
    # =========================
    def on_delete(self, req, resp, id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        DELETE FROM informasi_lembaga
        WHERE id = %s
        """, (id,))

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message": "Informasi berhasil dihapus"
        }