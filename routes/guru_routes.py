from resources.ManajemenGuru.jadwalmengajar import (
    JadwalMengajarResource,
    JadwalMengajarByIdResource
)

from resources.ManajemenGuru.matapelajaran import (
    MataPelajaranResource,
    MataPelajaranByIdResource
)


def register_guru_routes(app):

    # JADWAL MENGAJAR
    app.add_route("/jadwalmengajar", JadwalMengajarResource())
    app.add_route("/jadwalmengajar/{id:int}", JadwalMengajarByIdResource())

    # MATA PELAJARAN
    app.add_route("/matapelajaran", MataPelajaranResource())
    app.add_route("/matapelajaran/{id:int}", MataPelajaranByIdResource())