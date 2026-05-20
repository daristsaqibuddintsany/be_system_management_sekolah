import os
import json
import falcon

from datetime import date, datetime

from models.schema import init_db

# =========================
# IMPORT RESOURCES
# =========================

from resources.ManajemenUser.users import (
    LoginUser,
    RegisterUser
)

# MANAJEMEN SISWA
from resources.ManajemenSiswa.datasiswa import (
    SiswaResource,
    SiswaByIdResource
)

from resources.ManajemenSiswa.datakelas import (
    DataKelasResource,
    DataKelasByIdResource
)


from resources.ManajemenSiswa.datajurusan import (
    DataJurusanResource,
    DataJurusanByIdResource
)

from resources.ManajemenSiswa.aspekpenilaian import (
    AspekPenilaianResource,
    AspekPenilaianByIdResource
)

from resources.ManajemenSiswa.extracurricular import (
    ExtracurricularResource,
    ExtracurricularByIdResource
)

from resources.ManajemenSiswa.jenissemester import (
    JenisSemesterResource,
    JenisSemesterByIdResource
)

from resources.ManajemenSiswa.tahunajaran import (
    TahunAjaranResource,
    TahunAjaranByIdResource
)

from resources.ManajemenSiswa.walikelas import (
    WaliKelasResource,
    WaliKelasByIdResource
)

from resources.ManajemenSiswa.semester import (
    SemesterResource,
    SemesterByIdResource
)

from resources.ManajemenSiswa.dataraport import (
    DataRaportResource,
    DataRaportByIdResource
)

from resources.ManajemenSiswa.absensiharian import (
    AbsensiHarianResource,
    AbsensiHarianByIdResource
)

from resources.ManajemenSiswa.absensimapel import (
    AbsensiMapelResource,
    AbsensiMapelByIdResource
)

#=====================================================#




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



routes = [

    # AUTH
    ("/auth/login", LoginUser()),
    ("/auth/register", RegisterUser()),


# MANAJEMENSISWA
    # SISWA
    ("/siswa", SiswaResource()),
    ("/siswa/{id:int}", SiswaByIdResource()),

    # DATA KELAS
    ("/datakelas", DataKelasResource()),
    ("/datakelas/{id:int}", DataKelasByIdResource()),

    # DATA JURUSAN
    ("/datajurusan", DataJurusanResource()),
    ("/datajurusan/{id:int}", DataJurusanByIdResource()),

    # ASPEK PENILAIAN
    ("/aspekpenilaian", AspekPenilaianResource()),
    ("/aspekpenilaian/{id:int}", AspekPenilaianByIdResource()),

    # EXTRACURRICULAR
    ("/extracurricular", ExtracurricularResource()),
    ("/extracurricular/{id:int}", ExtracurricularByIdResource()),

    # JENIS SEMESTER
    ("/jenissemester", JenisSemesterResource()),
    ("/jenissemester/{id:int}", JenisSemesterByIdResource()),
    
    # TAHUN AJARAN
    ("/tahunajaran", TahunAjaranResource()),
    ("/tahunajaran/{id:int}", TahunAjaranByIdResource()),
    
    # WALI KELAS
   ("/walikelas", WaliKelasResource()),
   ("/walikelas/{id:int}", WaliKelasByIdResource()),
   
   # SEMESTER
   ("/semester", SemesterResource()),
   ("/semester/{id:int}", SemesterByIdResource()),
   
   # DATA RAPORT
("/dataraport", DataRaportResource()),
("/dataraport/{id:int}", DataRaportByIdResource()),

# ABSENSI HARIAN
("/absensiharian", AbsensiHarianResource()),
("/absensiharian/{id:int}", AbsensiHarianByIdResource()),

# ABSENSI MAPEL
("/absensimapel", AbsensiMapelResource()),
("/absensimapel/{id:int}", AbsensiMapelByIdResource()),

#==============================================================#
]

for route, resource in routes:

    app.add_route(
        route,
        resource
    )



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

# =========================
# START INFO
# =========================

print("🚀 APP RUNNING SUCCESSFULLY")
print(f"📂 Upload Directory: {UPLOAD_FOLDER}")

from wsgiref.simple_server import make_server

if __name__ == "__main__":
    print("🚀 Server running on http://127.0.0.1:8000")

    with make_server("127.0.0.1", 8000, app) as httpd:
        httpd.serve_forever()