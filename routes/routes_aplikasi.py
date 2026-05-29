from resources.ManajemenAplikasi.manajemenuser import (
    ManajemenUserResource
)

from resources.ManajemenAplikasi.informasilembaga import (
    InformasiLembagaResource
)

from resources.ManajemenAplikasi.backupdata import (
    BackupDataResource
)

from resources.ManajemenAplikasi.settinggps import (
    SettingGPSResource,
    SettingGPSByIdResource
)

from resources.ManajemenAplikasi.banneraplikasi import (
    BannerAplikasiResource,
    BannerAplikasiByIdResource
)

def register_aplikasi_routes(app):

   app.add_route(
    "/manajemen-user",
    ManajemenUserResource()
)

   app.add_route(
    "/manajemen-user/{id:int}",
    ManajemenUserResource()
)
   
   app.add_route(
    "/informasi-lembaga",
    InformasiLembagaResource()
)

   app.add_route(
    "/informasi-lembaga/{id:int}",
    InformasiLembagaResource()
)
   
   app.add_route(
    "/backup-data",
    BackupDataResource()
)
   
   app.add_route(
       "/setting-gps",
       SettingGPSResource()
)
   app.add_route(
       "/setting-gps/{id:int}",
       SettingGPSByIdResource()
)
   
   app.add_route(
       "/banner",
       BannerAplikasiResource()
)
   app.add_route(
       "/banner/{id:int}",
       BannerAplikasiByIdResource()
)