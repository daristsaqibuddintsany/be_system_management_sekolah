import falcon
from models.connection import get_connection


# =====================================================
# AUTO CREATE TABLE
# =====================================================

def create_daftar_pagu_table(cursor):

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS daftar_pagu (
        id INT AUTO_INCREMENT PRIMARY KEY,

        kode VARCHAR(30) NOT NULL,

        nama VARCHAR(100) NOT NULL,

        tahun VARCHAR(10) NOT NULL,

        nominal BIGINT NOT NULL DEFAULT 0,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ON UPDATE CURRENT_TIMESTAMP

    ) ENGINE=InnoDB
    """)


class DaftarPaguResource:

    # =====================================================
    # GET ALL
    # =====================================================

    def on_get(self, req, resp):

        tahun = req.get_param("tahun")
        search = req.get_param("search")

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # AUTO CREATE TABLE
        create_daftar_pagu_table(cursor)

        query = """
        SELECT *
        FROM daftar_pagu
        WHERE 1=1
        """

        values = []

        # FILTER TAHUN
        if tahun:

            query += " AND tahun=%s "
            values.append(tahun)

        # SEARCH
        if search:

            query += """
            AND (
                kode LIKE %s
                OR nama LIKE %s
            )
            """

            keyword = f"%{search}%"

            values.extend([keyword, keyword])

        query += """
        ORDER BY id DESC
        """

        cursor.execute(query, tuple(values))

        data = cursor.fetchall()

        cursor.close()
        conn.close()

        resp.media = {
            "data": data
        }

        resp.status = falcon.HTTP_200

    # =====================================================
    # CREATE
    # =====================================================

    def on_post(self, req, resp):

        body = req.media

        conn = get_connection()
        cursor = conn.cursor()

        # AUTO CREATE TABLE
        create_daftar_pagu_table(cursor)

        cursor.execute("""
        INSERT INTO daftar_pagu (

            kode,
            nama,
            tahun,
            nominal

        )
        VALUES (%s, %s, %s, %s)
        """, (

            body.get("kode"),
            body.get("nama"),
            body.get("tahun"),
            body.get("nominal", 0)

        ))

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message": "Data pagu berhasil ditambahkan"
        }

        resp.status = falcon.HTTP_201


class DaftarPaguByIdResource:

    # =====================================================
    # UPDATE
    # =====================================================

    def on_put(self, req, resp, id):

        body = req.media

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE daftar_pagu
        SET

            kode=%s,
            nama=%s,
            tahun=%s,
            nominal=%s

        WHERE id=%s
        """, (

            body.get("kode"),
            body.get("nama"),
            body.get("tahun"),
            body.get("nominal", 0),
            id

        ))

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message": "Data pagu berhasil diupdate"
        }

        resp.status = falcon.HTTP_200

    # =====================================================
    # DELETE
    # =====================================================

    def on_delete(self, req, resp, id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        DELETE FROM daftar_pagu
        WHERE id=%s
        """, (id,))

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message": "Data pagu berhasil dihapus"
        }

        resp.status = falcon.HTTP_200