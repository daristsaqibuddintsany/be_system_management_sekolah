from resources.ManajemenKeuangan.tunggakansiswa import (
    TunggakanSiswaResource,
    TunggakanSiswaByIdResource
)

from resources.ManajemenKeuangan.jenispembayaran import (
    JenisPembayaranResource,
    JenisPembayaranByIdResource
)

from resources.ManajemenKeuangan.tarifpembayaran import (
    TarifPembayaranResource,
    TarifPembayaranByIdResource
)

from resources.ManajemenKeuangan.rekappembayaran import (
    RekapPembayaranResource
)

from resources.ManajemenKeuangan.bayartagihan import (
    BayarTagihanResource,
    BayarTagihanCreateResource,
    BayarTagihanByIdResource
)

from resources.ManajemenKeuangan.transaksipembayaran import (
    TransaksiPembayaranResource,
    TransaksiPembayaranByIdResource,
    PrintTransaksiPembayaranResource
)

from resources.ManajemenKeuangan.rekapsiswa import (
    RekapSiswaResource,
    RekapSiswaByIdResource
)

from resources.ManajemenKeuangan.rekappertanggal import (
    RekapPerTanggalResource
)

from resources.ManajemenKeuangan.transaksitabunganteller import (
    TransaksiTabunganTellerResource,
    TransaksiTabunganTellerByIdResource
)

from resources.ManajemenKeuangan.riwayattabungan import (
    RiwayatTabunganResource
)


def register_keuangan_routes(app):

    # =========================
    # TUNGGAKAN SISWA
    # =========================
    app.add_route(
        "/tunggakan-siswa",
        TunggakanSiswaResource()
    )

    app.add_route(
        "/tunggakan-siswa/{id:int}",
        TunggakanSiswaByIdResource()
    )


    # =========================
    # JENIS PEMBAYARAN
    # =========================
    app.add_route(
        "/jenis-pembayaran",
        JenisPembayaranResource()
    )

    app.add_route(
        "/jenis-pembayaran/{id:int}",
        JenisPembayaranByIdResource()
    )


    # =========================
    # TARIF PEMBAYARAN
    # =========================
    app.add_route(
        "/tarif-pembayaran",
        TarifPembayaranResource()
    )

    app.add_route(
        "/tarif-pembayaran/{id:int}",
        TarifPembayaranByIdResource()
    )
    
    app.add_route(
        "/rekap-pembayaran",
        RekapPembayaranResource()
    )
    
    
    app.add_route("/bayar-tagihan", BayarTagihanResource())
    app.add_route("/bayar-tagihan/create", BayarTagihanCreateResource())
    app.add_route("/bayar-tagihan/{id:int}", BayarTagihanByIdResource())
    
    # =========================
    # TRANSAKSI PEMBAYARAN
    # =========================
    app.add_route(
        "/transaksi-pembayaran",
        TransaksiPembayaranResource()
    )

    app.add_route(
        "/transaksi-pembayaran/{id:int}",
        TransaksiPembayaranByIdResource()
    )

    app.add_route(
        "/transaksi-pembayaran/print/{id:int}",
        PrintTransaksiPembayaranResource()
    )
    
        # =========================================
    # REKAP SISWA
    # =========================================

    app.add_route(
        "/rekap-siswa",
        RekapSiswaResource()
    )

    app.add_route(
        "/rekap-siswa/{id:int}",
        RekapSiswaByIdResource()
    )
    
    # =========================================
    # REKAP PER TANGGAL
    # =========================================

    app.add_route(
        "/rekap-per-tanggal",
        RekapPerTanggalResource()
    )
    
    app.add_route(
    "/transaksi-tabungan-teller",
    TransaksiTabunganTellerResource()
    )

    app.add_route(
    "/transaksi-tabungan-teller/{id}",
    TransaksiTabunganTellerByIdResource()
    )
    
    app.add_route(
    "/riwayat-tabungan",
    RiwayatTabunganResource()
)