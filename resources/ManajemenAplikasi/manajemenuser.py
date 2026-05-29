import falcon

from models.connection import get_connection


class ManajemenUserResource:

    # =====================================================
    # GET ALL / FILTER USER
    # =====================================================
    def on_get(self, req, resp):

        jenis_user = req.get_param("jenis_user")
        kelas = req.get_param("kelas")

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT *
        FROM manajemen_user
        WHERE 1=1
        """

        values = []

        if jenis_user:
            query += " AND jenis_user = %s"
            values.append(jenis_user)

        if kelas:
            query += " AND kelas = %s"
            values.append(kelas)

        query += " ORDER BY id DESC"

        cursor.execute(query, tuple(values))
        data = cursor.fetchall()

        cursor.close()
        conn.close()

        resp.media = data


    # =====================================================
    # INSERT USER
    # =====================================================
    def on_post(self, req, resp):

        data = req.media

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO manajemen_user (
            jenis_user,
            nis_id,
            nama,
            kelas,
            password
        ) VALUES (%s, %s, %s, %s, %s)
        """, (
            data["jenis_user"],
            data["nis_id"],
            data["nama"],
            data.get("kelas"),
            data.get("password", "")
        ))

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message": "User berhasil ditambahkan"
        }


    # =====================================================
    # UPDATE PASSWORD (1 USER BY ID)
    # =====================================================
    def on_put(self, req, resp, id=None):

        data = req.media

        conn = get_connection()
        cursor = conn.cursor()

        # =========================
        # JIKA ADA ID → UPDATE 1 USER
        # =========================
        if id:

            cursor.execute("""
            UPDATE manajemen_user
            SET password = %s
            WHERE id = %s
            """, (
                data["password"],
                id
            ))

            message = "Password user berhasil diupdate"

        # =========================
        # JIKA TANPA ID → BULK UPDATE
        # =========================
        else:

            jenis_user = data.get("jenis_user")
            kelas = data.get("kelas")
            password = data.get("password")

            query = """
            UPDATE manajemen_user
            SET password = %s
            WHERE 1=1
            """

            values = [password]

            if jenis_user:
                query += " AND jenis_user = %s"
                values.append(jenis_user)

            if kelas:
                query += " AND kelas = %s"
                values.append(kelas)

            cursor.execute(query, tuple(values))

            message = "Password user berhasil diupdate (bulk)"

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message": message
        }