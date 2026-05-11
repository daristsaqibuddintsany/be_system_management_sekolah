import json
import falcon

from datetime import date, datetime

from models.schema import init_db
from resources.users import LoginUser, RegisterUser
from resources.ManajemenSiswa.datasiswa import SiswaResource


# =========================
# JSON SERIALIZER
# =========================
def json_serializer(obj):
    if isinstance(obj, (date, datetime)):
        return obj.isoformat()

    raise TypeError(f"Type {type(obj)} not serializable")


# =========================
# CORS MIDDLEWARE
# =========================
class CORSMiddleware:

    def process_request(self, req, resp):

        resp.set_header("Access-Control-Allow-Origin", "*")

        resp.set_header(
            "Access-Control-Allow-Headers",
            "Content-Type, Authorization"
        )

        resp.set_header(
            "Access-Control-Allow-Methods",
            "GET, POST, PUT, DELETE, OPTIONS"
        )

        if req.method == "OPTIONS":
            resp.status = falcon.HTTP_200
            resp.complete = True

    def process_response(self, req, resp, resource, req_succeeded):

        resp.set_header("Access-Control-Allow-Origin", "*")


# =========================
# INIT DATABASE
# =========================
init_db()


# =========================
# APP INIT
# =========================
app = falcon.App(
    middleware=[CORSMiddleware()]
)


# =========================
# JSON HANDLER
# =========================
app.resp_options.media_handlers[
    falcon.MEDIA_JSON
] = falcon.media.JSONHandler(
    dumps=lambda obj: json.dumps(
        obj,
        default=json_serializer
    )
)


# =========================
# ROUTES
# =========================

# AUTH
app.add_route("/auth/login", LoginUser())
app.add_route("/auth/register", RegisterUser())

app.add_route("/siswa", SiswaResource())
# =========================
# TEST ROUTE
# =========================
class TestResource:

    def on_get(self, req, resp):

        resp.media = {
            "status": True,
            "message": "Backend berjalan"
        }


app.add_route("/test", TestResource())


print("🚀 APP RUNNING SUCCESSFULLY")