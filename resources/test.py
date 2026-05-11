from models.schema import get_connection
import falcon

class TestResource:
    def on_get(self, req, resp):
        conn = None
        cursor = None

        try:
            conn = get_connection()        # <-- WAJIB dari schema.py
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()

            resp.status = falcon.HTTP_200
            resp.text = f"MySQL Connected: {result}"

        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.text = f"ERROR: {str(e)}"
            print("ERROR DETAIL:", e)

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()