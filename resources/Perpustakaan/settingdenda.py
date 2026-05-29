from models.connection import get_connection


class SettingDendaResource:

    # =========================
    # GET SETTING
    # =========================
    def on_get(self, req, resp):

        conn = get_connection()

        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
        SELECT *
        FROM setting_denda
        LIMIT 1
        """)

        data = cursor.fetchone()

        cursor.close()
        conn.close()

        resp.media = data


    # =========================
    # UPDATE DENDA
    # =========================
    def on_put(self, req, resp):

        data = req.media

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
        UPDATE setting_denda
        SET denda_per_hari = %s
        WHERE id = 1
        """, (
            data["denda_per_hari"],
        ))

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message": "Setting denda berhasil diupdate"
        }