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


def register_siswa_routes(app):

    # SISWA
    app.add_route("/siswa", SiswaResource())
    app.add_route("/siswa/{id:int}", SiswaByIdResource())

    # DATA KELAS
    app.add_route("/datakelas", DataKelasResource())
    app.add_route("/datakelas/{id:int}", DataKelasByIdResource())

    # DATA JURUSAN
    app.add_route("/datajurusan", DataJurusanResource())
    app.add_route("/datajurusan/{id:int}", DataJurusanByIdResource())

    # ASPEK PENILAIAN
    app.add_route("/aspekpenilaian", AspekPenilaianResource())
    app.add_route("/aspekpenilaian/{id:int}", AspekPenilaianByIdResource())

    # EXTRACURRICULAR
    app.add_route("/extracurricular", ExtracurricularResource())
    app.add_route("/extracurricular/{id:int}", ExtracurricularByIdResource())

    # JENIS SEMESTER
    app.add_route("/jenissemester", JenisSemesterResource())
    app.add_route("/jenissemester/{id:int}", JenisSemesterByIdResource())

    # TAHUN AJARAN
    app.add_route("/tahunajaran", TahunAjaranResource())
    app.add_route("/tahunajaran/{id:int}", TahunAjaranByIdResource())

    # WALI KELAS
    app.add_route("/walikelas", WaliKelasResource())
    app.add_route("/walikelas/{id:int}", WaliKelasByIdResource())

    # SEMESTER
    app.add_route("/semester", SemesterResource())
    app.add_route("/semester/{id:int}", SemesterByIdResource())

    # DATA RAPORT
    app.add_route("/dataraport", DataRaportResource())
    app.add_route("/dataraport/{id:int}", DataRaportByIdResource())

    # ABSENSI HARIAN
    app.add_route("/absensiharian", AbsensiHarianResource())
    app.add_route("/absensiharian/{id:int}", AbsensiHarianByIdResource())

    # ABSENSI MAPEL
    app.add_route("/absensimapel", AbsensiMapelResource())
    app.add_route("/absensimapel/{id:int}", AbsensiMapelByIdResource())