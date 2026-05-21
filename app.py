import os
import json
import falcon

from datetime import date, datetime

from models.schema import init_db



from resources.ManajemenUser.users import (
    LoginUser,
    RegisterUser
)



from routes.siswa_routes import register_siswa_routes
from routes.guru_routes import register_guru_routes
from routes.keuangan_routes import register_keuangan_routes


BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../../"
    )
)

UPLOAD_FOLDER = os.path.join(
    BASE_DIR,
    "uploads"
)

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


def json_serializer(obj):

    if isinstance(obj, (date, datetime)):
        return obj.isoformat()

    raise TypeError(
        f"Type {type(obj)} not serializable"
    )


class CORSMiddleware:

    def process_request(self, req, resp):

        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS"
        }

        for key, value in headers.items():
            resp.set_header(key, value)

        if req.method == "OPTIONS":

            resp.status = falcon.HTTP_200
            resp.complete = True

    def process_response(
        self,
        req,
        resp,
        resource,
        req_succeeded
    ):

        resp.set_header(
            "Access-Control-Allow-Origin",
            "*"
        )




init_db()




app = falcon.App(
    middleware=[CORSMiddleware()]
)




app.req_options.media_handlers.update({
    "multipart/form-data":
    falcon.media.MultipartFormHandler()
})




app.resp_options.media_handlers[
    falcon.MEDIA_JSON
] = falcon.media.JSONHandler(
    dumps=lambda obj: json.dumps(
        obj,
        default=json_serializer
    )
)




app.add_static_route(
    "/uploads",
    UPLOAD_FOLDER
)




app.add_route(
    "/auth/login",
    LoginUser()
)

app.add_route(
    "/auth/register",
    RegisterUser()
)


register_siswa_routes(app)


register_guru_routes(app)

register_keuangan_routes(app)

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




print("🚀 APP RUNNING SUCCESSFULLY")
print(f"📂 Upload Directory: {UPLOAD_FOLDER}")