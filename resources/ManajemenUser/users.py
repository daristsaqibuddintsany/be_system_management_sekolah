# resources/users.py

import falcon
import hashlib

from models.schema import get_connection


# =====================================
# HASH PASSWORD
# =====================================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# =====================================
# LOGIN
# =====================================
class LoginUser:

    def on_post(self, req, resp):

        conn = None
        cursor = None

        try:

            data = req.media or {}

            email = data.get("email", "").strip().lower()
            password = data.get("password", "").strip()

            if not email or not password:

                resp.media = {
                    "status": False,
                    "message": "Email dan password wajib diisi"
                }

                resp.status = falcon.HTTP_400
                return

            conn = get_connection()

            cursor = conn.cursor(dictionary=True)

            # AUTO BUAT ADMIN
            cursor.execute(
                "SELECT * FROM users WHERE email=%s",
                ("admin@gmail.com",)
            )

            admin = cursor.fetchone()

            if not admin:

                cursor.execute(
                    """
                    INSERT INTO users (
                        nama,
                        email,
                        password
                    )
                    VALUES (%s, %s, %s)
                    """,
                    (
                        "Admin",
                        "admin@gmail.com",
                        hash_password("123")
                    )
                )

                conn.commit()

            # LOGIN USER
            cursor.execute(
                """
                SELECT *
                FROM users
                WHERE email=%s
                """,
                (email,)
            )

            user = cursor.fetchone()

            # EMAIL TIDAK ADA
            if not user:

                resp.media = {
                    "status": False,
                    "message": "Email tidak ditemukan"
                }

                resp.status = falcon.HTTP_401
                return

            # PASSWORD SALAH
            if user["password"] != hash_password(password):

                resp.media = {
                    "status": False,
                    "message": "Password salah"
                }

                resp.status = falcon.HTTP_401
                return

            # LOGIN BERHASIL
            resp.media = {
                "status": True,
                "message": "Login berhasil",
                "token": "dummy-token",
                "user": {
                    "id": user["id"],
                    "nama": user["nama"],
                    "email": user["email"]
                }
            }

            resp.status = falcon.HTTP_200

        except Exception as e:

            resp.media = {
                "status": False,
                "message": str(e)
            }

            resp.status = falcon.HTTP_500

        finally:

            if cursor:
                cursor.close()

            if conn:
                conn.close()


# =====================================
# REGISTER
# =====================================
class RegisterUser:

    def on_post(self, req, resp):

        conn = None
        cursor = None

        try:

            data = req.media or {}

            nama = data.get("nama", "").strip()
            email = data.get("email", "").strip().lower()
            password = data.get("password", "").strip()

            if not nama or not email or not password:

                resp.media = {
                    "status": False,
                    "message": "Semua field wajib diisi"
                }

                resp.status = falcon.HTTP_400
                return

            conn = get_connection()

            cursor = conn.cursor(dictionary=True)

            # CEK EMAIL
            cursor.execute(
                "SELECT * FROM users WHERE email=%s",
                (email,)
            )

            user = cursor.fetchone()

            if user:

                resp.media = {
                    "status": False,
                    "message": "Email sudah digunakan"
                }

                resp.status = falcon.HTTP_400
                return

            # INSERT USER
            cursor.execute(
                """
                INSERT INTO users (
                    nama,
                    email,
                    password
                )
                VALUES (%s, %s, %s)
                """,
                (
                    nama,
                    email,
                    hash_password(password)
                )
            )

            conn.commit()

            resp.media = {
                "status": True,
                "message": "Register berhasil"
            }

            resp.status = falcon.HTTP_201

        except Exception as e:

            resp.media = {
                "status": False,
                "message": str(e)
            }

            resp.status = falcon.HTTP_500

        finally:

            if cursor:
                cursor.close()

            if conn:
                conn.close()