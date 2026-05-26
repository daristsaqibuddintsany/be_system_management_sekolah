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

from resources.ManajemenKeuangan.riwayattransaksi import (
    RiwayatTransaksiResource
)

from resources.ManajemenKeuangan.transaksipenerima import (
    TransaksiPenerimaanResource,
    TransaksiPenerimaanByIdResource
)

from resources.ManajemenKeuangan.jenispenerimaan import (
    JenisPenerimaanResource,
    JenisPenerimaanByIdResource
)

from resources.ManajemenKeuangan.jenispembayaran import (
    JenisPembayaranResource,
    JenisPembayaranByIdResource
)

from resources.ManajemenKeuangan.laporanpenerimaan import (
    LaporanPenerimaanResource,
    LaporanPenerimaanByIdResource
)

from resources.ManajemenKeuangan.transaksipengeluaran import (
    TransaksiPengeluaranResource,
    TransaksiPengeluaranByIdResource
)

from resources.ManajemenKeuangan.jenispengeluaran import (
    JenisPengeluaranResource,
    JenisPengeluaranByIdResource
)

from resources.ManajemenKeuangan.laporanpengeluaran import LaporanPengeluaranResource

from resources.ManajemenKeuangan.transaksipenjurnalan import (
    TransaksiJurnalResource,
    TransaksiJurnalByIdResource
)

from resources.ManajemenKeuangan.laporanjurnal import (
    LaporanJurnalResource,
    LaporanJurnalByIdResource
)

from resources.ManajemenKeuangan.neracasaldo import NeracaSaldoResource

from resources.ManajemenKeuangan.jurnalumum import JurnalUmumResource

from resources.ManajemenKeuangan.penghasilankomprehensif import PenghasilanKomprehensifResource

from resources.ManajemenKeuangan.posisikeuangan import PosisiKeuanganResource

from resources.ManajemenKeuangan.aruskas import ArusKasResource

from resources.ManajemenKeuangan.perubahanasetneto import PerubahanAsetNetoResource

from resources.ManajemenKeuangan.realisasipenerimaan import (
    RealisasiPenerimaanResource,
    RealisasiPenerimaanByIdResource
)

from resources.ManajemenKeuangan.realisasibelanja import (
    RealisasiBelanjaResource,
    RealisasiBelanjaByIdResource
)

from resources.ManajemenKeuangan.daftarpagu import (
    DaftarPaguResource,
    DaftarPaguByIdResource
)

from resources.ManajemenKeuangan.rekapitulasiapbs import (
    RekapitulasiAPBSResource
)

from resources.ManajemenKeuangan.apbddetail import (
    APBDDetailResource
)

from resources.ManajemenKeuangan.realisasianggaran import (
    RealisasiAnggaranResource,
    RealisasiAnggaranByIdResource
)

from resources.ManajemenKeuangan.evaluasianggaran import (
    EvaluasiAnggaranResource,
    EvaluasiAnggaranByIdResource
)

from resources.ManajemenKeuangan.akunbudgeting import (
    AkunBudgetingResource,
    AkunBudgetingByIdResource
)

from resources.ManajemenKeuangan.akunkeuangan import (
    AkunKeuanganResource,
    AkunKeuanganByIdResource
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
    
    app.add_route(
    "/transaksi",
    RiwayatTransaksiResource()
)
    
    app.add_route(
    "/transaksi-penerimaan",
    TransaksiPenerimaanResource()
)

    app.add_route(
    "/transaksi-penerimaan/{id}",
    TransaksiPenerimaanByIdResource()
)
    
    app.add_route(
    "/jenis-penerimaan",
    JenisPenerimaanResource()
)

    app.add_route(
    "/jenis-penerimaan/{id:int}",
    JenisPenerimaanByIdResource()
)
    app.add_route(
    "/jenis-pembayaran",
    JenisPembayaranResource()
)

    app.add_route(
    "/jenis-pembayaran/{id:int}",
    JenisPembayaranByIdResource()
)
    
    app.add_route(
    "/laporan-penerimaan",
    LaporanPenerimaanResource()
)

    app.add_route(
    "/laporan-penerimaan/{id:int}",
    LaporanPenerimaanByIdResource()
)
    
    app.add_route(
    "/transaksi-pengeluaran", 
    TransaksiPengeluaranResource()
)

    app.add_route(
    "/transaksi-pengeluaran/{id:int}", 
    TransaksiPengeluaranByIdResource()
)
    
    app.add_route(
    "/jenis-pengeluaran", 
    JenisPengeluaranResource()
)

    app.add_route(
    "/jenis-pengeluaran/{id:int}", 
    JenisPengeluaranByIdResource()
)
    app.add_route(
    "/pengeluaran", 
    LaporanPengeluaranResource()
)
    
    app.add_route(
    "/api/transaksi-jurnal", 
    TransaksiJurnalResource()
)

    app.add_route(
    "/api/transaksi-jurnal/{id:int}", 
    TransaksiJurnalByIdResource()
)
    
    app.add_route(
    "/api/transaksi-jurnal",
    LaporanJurnalResource()
)
    
    app.add_route(
    "/api/transaksi-jurnal/{id:int}",
    LaporanJurnalByIdResource()
)
    
    app.add_route(
    "/buku-besar-ringkasan",
    NeracaSaldoResource()
)
    
    app.add_route(
    "/jurnal-umum", 
    JurnalUmumResource()
)
    
    app.add_route(
    "/penghasilan-komprehensif", 
    PenghasilanKomprehensifResource()
)
    
    app.add_route(
    "/posisi-keuangan", 
    PosisiKeuanganResource()
)
    
    app.add_route(
    "/arus-kas", 
    ArusKasResource()
)
    
    app.add_route(
    "/perubahan-aset-neto", 
    PerubahanAsetNetoResource()
)
    
    app.add_route(
    "/realisasi-penerimaan",
    RealisasiPenerimaanResource()
)

    app.add_route(
    "/realisasi-penerimaan/{id:int}",
    RealisasiPenerimaanByIdResource()
)
    
    app.add_route(
    "/realisasi-belanja",
    RealisasiBelanjaResource()
)

    app.add_route(
    "/realisasi-belanja/{id:int}",
    RealisasiBelanjaByIdResource()
)
    
    app.add_route(
    "/daftar-pagu",
    DaftarPaguResource()
)

    app.add_route(
    "/daftar-pagu/{id:int}",
    DaftarPaguByIdResource()
)
    
    app.add_route(
    "/rekapitulasi-apbs",
    RekapitulasiAPBSResource()
)
    
    app.add_route(
    "/apbd-detail",
    APBDDetailResource()
)
    
    app.add_route(
    "/realisasi-anggaran",
    RealisasiAnggaranResource()
)

    app.add_route(
    "/realisasi-anggaran/{id:int}",
    RealisasiAnggaranByIdResource()
)
    
    app.add_route(
    "/evaluasi-anggaran",
    EvaluasiAnggaranResource()
)

    app.add_route(
    "/evaluasi-anggaran/{id:int}",
    EvaluasiAnggaranByIdResource()
)
    
    app.add_route(
    '/akunbudgeting',
    AkunBudgetingResource()
)

    app.add_route(
    '/akunbudgeting/{id:int}',
    AkunBudgetingByIdResource()
)
    
    app.add_route(
    '/akunkeuangan',
    AkunKeuanganResource()
)

    app.add_route(
    '/akunkeuangan/{id:int}',
    AkunKeuanganByIdResource()
) 