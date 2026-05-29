import os
import json
import falcon

from datetime import (
    date,
    datetime
)

from waitress import serve

from models.schema import init_db

from resources.ManajemenUser.users import (
    LoginUser,
    RegisterUser
)

from routes.siswa_routes import (
    register_siswa_routes
)

from routes.guru_routes import (
    register_guru_routes
)

# =========================================
# ROOT PROJECT
# =========================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

UPLOAD_FOLDER = os.path.join(
    BASE_DIR,
    "uploads"
)

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

print("📂 APP UPLOAD:", UPLOAD_FOLDER)

# =========================================
# JSON SERIALIZER
# =========================================

def json_serializer(obj):

    if isinstance(obj, (date, datetime)):
        return obj.isoformat()

    raise TypeError

# =========================================
# CORS
# =========================================

class CORSMiddleware:

    def process_request(self, req, resp):

        resp.set_header(
            "Access-Control-Allow-Origin",
            "*"
        )

        resp.set_header(
            "Access-Control-Allow-Headers",
            "*"
        )

        resp.set_header(
            "Access-Control-Allow-Methods",
            "*"
        )

        if req.method == "OPTIONS":

            resp.status = falcon.HTTP_200

            resp.complete = True

# =========================================
# INIT DB
# =========================================

init_db()

# =========================================
# APP
# =========================================

app = falcon.App(
    middleware=[CORSMiddleware()]
)

# =========================================
# MULTIPART
# =========================================

app.req_options.media_handlers.update({

    "multipart/form-data":
    falcon.media.MultipartFormHandler()

})

# =========================================
# JSON
# =========================================

app.resp_options.media_handlers[
    falcon.MEDIA_JSON
] = falcon.media.JSONHandler(

    dumps=lambda obj: json.dumps(
        obj,
        default=json_serializer
    )

)

# =========================================
# STATIC ROUTE
# =========================================

app.add_static_route(
    "/uploads",
    UPLOAD_FOLDER
)

print("✅ STATIC ROUTE AKTIF")

# =========================================
# AUTH
# =========================================

app.add_route(
    "/auth/login",
    LoginUser()
)

app.add_route(
    "/auth/register",
    RegisterUser()
)

# =========================================
# SISWA ROUTES
# =========================================

register_siswa_routes(app)

# =========================================
# GURU ROUTES
# =========================================

register_guru_routes(app)

# =========================================
# TEST
# =========================================

class TestResource:

    def on_get(self, req, resp):

        resp.media = {
            "status": True,
            "message": "Backend berjalan"
        }

app.add_route(
    "/test",
    TestResource()
)

# =========================================
# RUN SERVER
# =========================================

if __name__ == "__main__":

    print("🚀 SERVER RUNNING")
    print("📂 UPLOAD:", UPLOAD_FOLDER)

    serve(
        app,
        host="127.0.0.1",
        port=8000
    )