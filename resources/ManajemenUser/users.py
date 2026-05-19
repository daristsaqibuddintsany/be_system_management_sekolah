# resources/users.py

import falcon
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from models.schema import get_connection


# =====================================
# LOGIN
# =====================================
class LoginUser:

    # TEST GET
    def on_get(self, req, resp):

        resp.media = {
            "status": True,
            "message": "Endpoint login aktif"
        }

    # LOGIN POST
    def on_post(self, req, resp):

        conn = None
        cursor = None

        try:

            data = req.media

            email = data.get("email")
            password = data.get("password")

            # VALIDASI
            if not email or not password:

                resp.media = {
                    "status": False,
                    "message": "Email dan password wajib diisi"
                }

                resp.status = falcon.HTTP_400
                return

            conn = get_connection()

            cursor = conn.cursor(
                dictionary=True
            )

            # CARI USER
            cursor.execute(
                """
                SELECT * FROM users
                WHERE email=%s
                """,
                (email,)
            )

            user = cursor.fetchone()

            # USER TIDAK ADA
            if not user:

                resp.media = {
                    "status": False,
                    "message": "Email tidak ditemukan"
                }

                resp.status = falcon.HTTP_401
                return

            # CEK PASSWORD
            if not check_password_hash(
                user["password"],
                password
            ):

                resp.media = {
                    "status": False,
                    "message": "Password salah"
                }

                resp.status = falcon.HTTP_401
                return

            # BERHASIL LOGIN
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

    # TEST GET
    def on_get(self, req, resp):

        resp.media = {
            "status": True,
            "message": "Endpoint register aktif"
        }

    # REGISTER POST
    def on_post(self, req, resp):

        conn = None
        cursor = None

        try:

            data = req.media

            nama = data.get("nama")
            email = data.get("email")
            password = data.get("password")

            # VALIDASI
            if not nama or not email or not password:

                resp.media = {
                    "status": False,
                    "message": "Semua field wajib diisi"
                }

                resp.status = falcon.HTTP_400
                return

            conn = get_connection()

            cursor = conn.cursor(
                dictionary=True
            )

            # CEK EMAIL SUDAH ADA
            cursor.execute(
                """
                SELECT * FROM users
                WHERE email=%s
                """,
                (email,)
            )

            user_exist = cursor.fetchone()

            if user_exist:

                resp.media = {
                    "status": False,
                    "message": "Email sudah digunakan"
                }

                resp.status = falcon.HTTP_400
                return

            # HASH PASSWORD
            hashed_password = generate_password_hash(
                password
            )

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
                    hashed_password
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