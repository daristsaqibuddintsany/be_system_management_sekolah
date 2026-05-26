def create_keuangan_table(cursor):

    # =====================================================
    # JENIS PEMBAYARAN
    # =====================================================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS jenis_pembayaran (
        id INT AUTO_INCREMENT PRIMARY KEY,
        kode VARCHAR(30) UNIQUE NOT NULL,
        nama VARCHAR(100) NOT NULL,
        akun_harta VARCHAR(100) NOT NULL,
        akun_pendapatan VARCHAR(100) NOT NULL,
        akun_hutang VARCHAR(100) DEFAULT NULL,
        tipe ENUM('Bebas', 'Wajib') DEFAULT 'Wajib',
        status ENUM('aktif', 'nonaktif') DEFAULT 'aktif',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    ) ENGINE=InnoDB
    """)

    # =====================================================
    # TARIF PEMBAYARAN
    # =====================================================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tarif_pembayaran (
        id INT AUTO_INCREMENT PRIMARY KEY,
        siswa_id INT NOT NULL,
        nis VARCHAR(20) NOT NULL,
        nama_siswa VARCHAR(100) NOT NULL,
        kelas VARCHAR(50) NOT NULL,
        tahun_ajaran VARCHAR(20) NOT NULL,
        bulan VARCHAR(20) NOT NULL,
        nominal INT NOT NULL DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    ) ENGINE=InnoDB
    """)

    # =====================================================
# PEMBAYARAN
# =====================================================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pembayaran (
     id INT AUTO_INCREMENT PRIMARY KEY,
     no_kwitansi VARCHAR(50) UNIQUE,
     siswa_id INT NOT NULL,
     nis VARCHAR(20) NOT NULL,
     nama_siswa VARCHAR(100) NOT NULL,
     kelas VARCHAR(50) NOT NULL,
     jenis_pembayaran_id INT DEFAULT NULL,
     bulan VARCHAR(20) NOT NULL,
    tahun_ajaran VARCHAR(20) NOT NULL,
    jumlah_tagihan INT NOT NULL DEFAULT 0,
    jumlah_bayar INT NOT NULL DEFAULT 0,
        sisa_tagihan INT NOT NULL DEFAULT 0,
        metode_pembayaran VARCHAR(50) DEFAULT 'cash',
        keterangan TEXT DEFAULT NULL,
        status ENUM('lunas', 'cicil', 'belum', 'aktif') DEFAULT 'belum',
        tanggal_bayar DATE DEFAULT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        CONSTRAINT fk_pembayaran_jenis FOREIGN KEY (jenis_pembayaran_id)
        REFERENCES jenis_pembayaran(id) ON DELETE SET NULL
    ) ENGINE=InnoDB
    """)

    # -----------------------------------------------------
    # FORCE ALTER MIGRATION (Penyelamat Error 1054)
    # -----------------------------------------------------
    try:
        cursor.execute("ALTER TABLE pembayaran ADD COLUMN jumlah_tagihan INT NOT NULL DEFAULT 0 AFTER tahun_ajaran")
    except:
        pass

    try:
        cursor.execute("ALTER TABLE pembayaran ADD COLUMN jumlah_bayar INT NOT NULL DEFAULT 0 AFTER jumlah_tagihan")
    except:
        pass

    try:
        cursor.execute("ALTER TABLE pembayaran ADD COLUMN sisa_tagihan INT NOT NULL DEFAULT 0 AFTER jumlah_bayar")
    except:
        pass

 # =====================================================
# TUNGGAKAN SISWA
 # =====================================================
    cursor.execute("""
CREATE TABLE IF NOT EXISTS tunggakan_siswa (
     id INT AUTO_INCREMENT PRIMARY KEY,
     siswa_id INT NOT NULL,
    nis VARCHAR(20) NOT NULL,
     nama_siswa VARCHAR(100) NOT NULL,
     kelas VARCHAR(50) NOT NULL,
      tahun_ajaran VARCHAR(20) NOT NULL,
      bulan VARCHAR(20) NOT NULL,
        nominal INT NOT NULL DEFAULT 0,
        status ENUM('lunas', 'belum_lunas') DEFAULT 'belum_lunas',
        keterangan TEXT DEFAULT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    ) ENGINE=InnoDB
    """)

    # =====================================================
    # VIEW REKAP SISWA
    # =====================================================
    cursor.execute("""
    CREATE OR REPLACE VIEW view_rekap_siswa AS
    SELECT
        p.siswa_id,
        p.nis,
        p.nama_siswa,
        p.kelas,
        p.tahun_ajaran,
        SUM(p.jumlah_tagihan) AS total_tagihan,
        SUM(p.jumlah_bayar) AS total_bayar,
        SUM(p.sisa_tagihan) AS total_tunggakan
    FROM pembayaran p
    GROUP BY
        p.siswa_id,
        p.nis,
        p.nama_siswa,
        p.kelas,
        p.tahun_ajaran
    """)
    
    # =====================================================
    # TABUNGAN TELLER & RIWAYAT
    # =====================================================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transaksi_tabungan_teller (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nis VARCHAR(30) NOT NULL,
        jenis ENUM('Penyetoran', 'Penarikan') NOT NULL,
        nominal BIGINT NOT NULL DEFAULT 0,
        keterangan TEXT DEFAULT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    ) ENGINE=InnoDB
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transaksi_penerimaan (
        id INT AUTO_INCREMENT PRIMARY KEY,
        kode VARCHAR(50) UNIQUE,
        jenis VARCHAR(100) NOT NULL,
        sumber VARCHAR(150) NOT NULL,
        tanggal DATE NOT NULL,
        nominal BIGINT NOT NULL DEFAULT 0,
        menyetujui VARCHAR(100) DEFAULT NULL,
        keterangan TEXT DEFAULT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    ) ENGINE=InnoDB
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS riwayat_tabungan (
        id INT AUTO_INCREMENT PRIMARY KEY,
        transaksi_id INT DEFAULT NULL,
        nis VARCHAR(30) NOT NULL,
        nama_siswa VARCHAR(100) DEFAULT NULL,
        jenis ENUM('Setor', 'Tarik') NOT NULL,
        jumlah BIGINT NOT NULL DEFAULT 0,
        keterangan TEXT DEFAULT NULL,
        tanggal DATE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        CONSTRAINT fk_riwayat_tabungan FOREIGN KEY (transaksi_id)
        REFERENCES transaksi_tabungan_teller(id) ON DELETE CASCADE
    ) ENGINE=InnoDB
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS riwayat_transaksi (
        id INT AUTO_INCREMENT PRIMARY KEY,
        transaksi_id INT DEFAULT NULL,
        kode VARCHAR(50),
        jenis VARCHAR(50),
        nis VARCHAR(30),
        nama VARCHAR(100),
        jumlah BIGINT DEFAULT 0,
        keterangan TEXT DEFAULT NULL,
        tanggal DATE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        CONSTRAINT fk_riwayat_transaksi FOREIGN KEY (transaksi_id)
        REFERENCES transaksi_tabungan_teller(id) ON DELETE CASCADE
    ) ENGINE=InnoDB
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS jenis_penerimaan (
        id INT AUTO_INCREMENT PRIMARY KEY,
        akun_harta VARCHAR(100) NOT NULL,
        kode_keuangan VARCHAR(100) NOT NULL,
        kode VARCHAR(50) UNIQUE NOT NULL,
        nama VARCHAR(150) NOT NULL,
        jenis VARCHAR(100) NOT NULL,
        keterangan TEXT DEFAULT NULL,
        status ENUM('Aktif', 'Nonaktif') DEFAULT 'Aktif',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    ) ENGINE=InnoDB
    """)
    
    # =====================================================
    # REKAP PEMBAYARAN BULANAN SISWA
    # =====================================================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS rekap_pembayaran (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nis VARCHAR(30) NOT NULL,
        nama VARCHAR(100) NOT NULL,
        kelas VARCHAR(50) NOT NULL DEFAULT '',
        tahun VARCHAR(20) NOT NULL,
        tipe VARCHAR(50) NOT NULL DEFAULT '',
        jenis VARCHAR(100) NOT NULL,
        jan VARCHAR(20) DEFAULT '✖',
        feb VARCHAR(20) DEFAULT '✖',
        mar VARCHAR(20) DEFAULT '✖',
        apr VARCHAR(20) DEFAULT '✖',
        mei VARCHAR(20) DEFAULT '✖',
        jun VARCHAR(20) DEFAULT '✖',
        jul VARCHAR(20) DEFAULT '✖',
        ags VARCHAR(20) DEFAULT '✖',
        sep VARCHAR(20) DEFAULT '✖',
        okt VARCHAR(20) DEFAULT '✖',
        nov VARCHAR(20) DEFAULT '✖',
        des VARCHAR(20) DEFAULT '✖',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    ) ENGINE=InnoDB
    """)
    
    # =====================================================
    # REKAP PEMBAYARAN PER TANGGAL (HARIAN)
    # =====================================================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS rekap_per_tanggal (
        id INT AUTO_INCREMENT PRIMARY KEY,
        tanggal DATE NOT NULL,
        no_kwitansi VARCHAR(50) NOT NULL,
        nis VARCHAR(30) NOT NULL,
        nama VARCHAR(100) NOT NULL,
        kelas VARCHAR(50) NOT NULL,
        petugas VARCHAR(100) NOT NULL,
        nominal BIGINT NOT NULL DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    ) ENGINE=InnoDB
    """)
    
    # =====================================================
    # TRANSAKSI PENGELUARAN (DIBUTUHKAN OLEH LAPORAN PENERIMAAN)
    # =====================================================

    
    cursor.execute("""
CREATE TABLE IF NOT EXISTS transaksi_pengeluaran (
    id INT AUTO_INCREMENT PRIMARY KEY,
    kode VARCHAR(50) UNIQUE NOT NULL,
    jenis VARCHAR(150) NOT NULL,
    bidang VARCHAR(100) DEFAULT NULL,
    penerima VARCHAR(150) DEFAULT NULL,
    sumber VARCHAR(100) DEFAULT NULL,
    tanggal DATE NOT NULL,
    menyetujui VARCHAR(150) DEFAULT NULL,
    keterangan TEXT DEFAULT NULL,
    nominal BIGINT NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB
""")
    
    cursor.execute("""
CREATE TABLE IF NOT EXISTS jenis_pengeluaran (
    id INT AUTO_INCREMENT PRIMARY KEY,
    kode_keuangan VARCHAR(50) NOT NULL,
    kode_pengeluaran VARCHAR(50) UNIQUE NOT NULL,
    nama VARCHAR(150) NOT NULL,
    jenis ENUM('Dengan Pembatasan', 'Tanpa Pembatasan') NOT NULL,
    keterangan TEXT DEFAULT NULL,
    status ENUM('Aktif', 'Nonaktif') NOT NULL DEFAULT 'Aktif',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB
""")

    cursor.execute("""
CREATE TABLE IF NOT EXISTS transaksi_pengeluaran (
    id INT AUTO_INCREMENT PRIMARY KEY,
    kode VARCHAR(50) UNIQUE NOT NULL,
    jenis VARCHAR(150) NOT NULL,
    bidang VARCHAR(100) DEFAULT NULL,
    penerima VARCHAR(150) DEFAULT NULL,
    sumber VARCHAR(100) DEFAULT NULL,
    petugas VARCHAR(100) DEFAULT NULL, -- Kolom baru penyesuaian React Laporan
    tanggal DATE NOT NULL,
    menyetujui VARCHAR(150) DEFAULT NULL,
    keterangan TEXT DEFAULT NULL,
    nominal BIGINT NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB
""")
    
    cursor.execute("""
CREATE TABLE IF NOT EXISTS akun (
    id INT AUTO_INCREMENT PRIMARY KEY,
    kode_akun VARCHAR(50) UNIQUE NOT NULL,
    nama_akun VARCHAR(150) NOT NULL,
    kategori VARCHAR(100) DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB
""")
    

    cursor.execute("""
CREATE TABLE IF NOT EXISTS jurnal (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tanggal DATE NOT NULL,
    keperluan VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB
""")
    
    

# Tabel Detail Jurnal (Banyak baris akun per Jurnal)
    cursor.execute("""
CREATE TABLE IF NOT EXISTS jurnal_detail (
    id INT AUTO_INCREMENT PRIMARY KEY,
    jurnal_id INT NOT NULL,
    akun_id INT NOT NULL,
    debit BIGINT NOT NULL DEFAULT 0,
    kredit BIGINT NOT NULL DEFAULT 0,

    CONSTRAINT fk_jurnal_detail_jurnal
        FOREIGN KEY (jurnal_id)
        REFERENCES jurnal(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_jurnal_detail_akun
        FOREIGN KEY (akun_id)
        REFERENCES akun(id)
        ON DELETE CASCADE

) ENGINE=InnoDB
""")
    
    cursor.execute("""
CREATE TABLE IF NOT EXISTS laporan_jurnal (
    id INT AUTO_INCREMENT PRIMARY KEY,
    kode VARCHAR(50) UNIQUE NOT NULL,
    tanggal DATE NOT NULL,
    keperluan TEXT DEFAULT NULL,
    petugas VARCHAR(100) DEFAULT NULL,
    debit BIGINT NOT NULL DEFAULT 0,
    kredit BIGINT NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB
""")
    
    # Query mengagregasi data dari jurnal_detail dan akun berdasarkan filter tanggal
# Jalankan query otomatisasi Buku Besar Ringkasan
    cursor.execute("""
CREATE TABLE IF NOT EXISTS laporan_buku_besar (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tanggal_awal DATE NOT NULL,
    tanggal_akhir DATE NOT NULL,
    kode_akun VARCHAR(50) NOT NULL,
    nama_akun VARCHAR(150) NOT NULL,
    debit BIGINT NOT NULL DEFAULT 0,
    kredit BIGINT NOT NULL DEFAULT 0,
    saldo_akhir BIGINT NOT NULL DEFAULT 0,
    petugas VARCHAR(100) DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_buku_besar_akun FOREIGN KEY (kode_akun) REFERENCES akun(kode_akun) ON DELETE CASCADE
) ENGINE=InnoDB
""")
    
    cursor.execute("""
CREATE TABLE IF NOT EXISTS neraca_saldo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tanggal_awal DATE NOT NULL,
    tanggal_akhir DATE NOT NULL,
    kode_akun VARCHAR(50) NOT NULL,
    nama_akun VARCHAR(150) NOT NULL,
    debit BIGINT NOT NULL DEFAULT 0,
    kredit BIGINT NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_neraca_saldo_akun FOREIGN KEY (kode_akun) REFERENCES akun(kode_akun) ON DELETE CASCADE
) ENGINE=InnoDB
""")
    
    cursor.execute("""
CREATE TABLE IF NOT EXISTS laporan_jurnal_umum (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tanggal DATE NOT NULL,
    kode_transaksi VARCHAR(50) NOT NULL,
    kode_akun VARCHAR(50) NOT NULL,
    nama_akun VARCHAR(150) NOT NULL,
    debit BIGINT NOT NULL DEFAULT 0,
    kredit BIGINT NOT NULL DEFAULT 0,
    keterangan TEXT DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_laporan_jurnal_akun FOREIGN KEY (kode_akun) REFERENCES akun(kode_akun) ON DELETE CASCADE
) ENGINE=InnoDB
""")
    
    cursor.execute("""
CREATE TABLE IF NOT EXISTS laporan_penghasilan_komprehensif (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tanggal DATE NOT NULL,
    nama_akun VARCHAR(150) NOT NULL,
    tipe ENUM('Pendapatan', 'Beban') NOT NULL,
    dengan_pembatasan BIGINT NOT NULL DEFAULT 0,
    tanpa_pembatasan BIGINT NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB
""")
    
    cursor.execute("""
CREATE TABLE IF NOT EXISTS laporan_posisi_keuangan (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tanggal DATE NOT NULL,
    nama_akun VARCHAR(150) NOT NULL,
    kategori ENUM('Aset', 'Liabilitas') NOT NULL,
    nominal BIGINT NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB
""")
    
    cursor.execute("""
CREATE TABLE IF NOT EXISTS laporan_arus_kas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tanggal DATE NOT NULL,
    nama_akun VARCHAR(150) NOT NULL,
    aktivitas ENUM('Operasi', 'Investasi', 'Pendanaan') NOT NULL,
    nominal BIGINT NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB
""")
    
    cursor.execute("""
CREATE TABLE IF NOT EXISTS laporan_perubahan_aset_neto (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tahun INT NOT NULL,
    aset_neto_dengan_pembatasan BIGINT NOT NULL DEFAULT 0,
    aset_neto_tanpa_pembatasan BIGINT NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB
""")
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS realisasi_penerimaan (
        id INT AUTO_INCREMENT PRIMARY KEY,

        kode_akun VARCHAR(30) NOT NULL,
        nama_akun VARCHAR(100) NOT NULL,

        bulan VARCHAR(20) NOT NULL,

        tahun_ajaran VARCHAR(20) NOT NULL,

        nominal BIGINT NOT NULL DEFAULT 0,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ON UPDATE CURRENT_TIMESTAMP

    ) ENGINE=InnoDB
    """)
    
    # =====================================================
# REALISASI BELANJA
# =====================================================

    cursor.execute("""
CREATE TABLE IF NOT EXISTS realisasi_belanja (
    id INT AUTO_INCREMENT PRIMARY KEY,

    kode_akun VARCHAR(30) NOT NULL,
    nama_akun VARCHAR(100) NOT NULL,

    bulan VARCHAR(20) NOT NULL,

    tahun_ajaran VARCHAR(20) NOT NULL,

    nominal BIGINT NOT NULL DEFAULT 0,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP

) ENGINE=InnoDB
""")
    
    # =====================================================
# DAFTAR PAGU
# =====================================================

    cursor.execute("""
CREATE TABLE IF NOT EXISTS daftar_pagu (
    id INT AUTO_INCREMENT PRIMARY KEY,

    kode VARCHAR(30) NOT NULL,

    nama VARCHAR(100) NOT NULL,

    tahun VARCHAR(10) NOT NULL,

    nominal BIGINT NOT NULL DEFAULT 0,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP

) ENGINE=InnoDB
""")
    
    # =====================================================
# APBS INDUK
# =====================================================

    cursor.execute("""
CREATE TABLE IF NOT EXISTS apbs_induk (
    id INT AUTO_INCREMENT PRIMARY KEY,

    jenis ENUM(
        'pendapatan',
        'belanja'
    ) NOT NULL,

    kode_akun VARCHAR(30) NOT NULL,

    nama_akun VARCHAR(100) NOT NULL,

    tahun_ajaran VARCHAR(20) NOT NULL,

    total_realisasi BIGINT NOT NULL DEFAULT 0,

    saldo_awal BIGINT NOT NULL DEFAULT 0,

    saldo_berjalan BIGINT NOT NULL DEFAULT 0,

    proyeksi_akhir_tahun BIGINT NOT NULL DEFAULT 0,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP

) ENGINE=InnoDB
""")

# =====================================================
# APBD DETAIL
# =====================================================

    cursor.execute("""
CREATE TABLE IF NOT EXISTS apbd_detail (
    id INT AUTO_INCREMENT PRIMARY KEY,

    jenis ENUM(
        'pendapatan',
        'belanja'
    ) NOT NULL,

    kode_akun VARCHAR(30) NOT NULL,

    nama_akun VARCHAR(100) NOT NULL,

    tahun_ajaran VARCHAR(20) NOT NULL,

    bulan VARCHAR(20) NOT NULL,

    nominal BIGINT NOT NULL DEFAULT 0,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP

) ENGINE=InnoDB
""")
    
    # =====================================================
# REALISASI ANGGARAN BULANAN
# =====================================================

    cursor.execute("""
CREATE TABLE IF NOT EXISTS realisasi_anggaran (
    id INT AUTO_INCREMENT PRIMARY KEY,

    kode_akun VARCHAR(30) NOT NULL,
    nama_akun VARCHAR(150) NOT NULL,

    kategori ENUM(
        'pendapatan',
        'belanja'
    ) NOT NULL,

    tahun_ajaran VARCHAR(20) NOT NULL,

    pagu DECIMAL(18,2) DEFAULT 0,

    juli DECIMAL(18,2) DEFAULT 0,
    agustus DECIMAL(18,2) DEFAULT 0,
    september DECIMAL(18,2) DEFAULT 0,
    oktober DECIMAL(18,2) DEFAULT 0,
    november DECIMAL(18,2) DEFAULT 0,
    desember DECIMAL(18,2) DEFAULT 0,
    januari DECIMAL(18,2) DEFAULT 0,
    februari DECIMAL(18,2) DEFAULT 0,
    maret DECIMAL(18,2) DEFAULT 0,
    april DECIMAL(18,2) DEFAULT 0,
    mei DECIMAL(18,2) DEFAULT 0,
    juni DECIMAL(18,2) DEFAULT 0,

    total_realisasi DECIMAL(18,2) GENERATED ALWAYS AS (
        juli + agustus + september +
        oktober + november + desember +
        januari + februari + maret +
        april + mei + juni
    ) STORED,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP
)
""")
    
    # =====================================================
# EVALUASI ANGGARAN
# =====================================================

    cursor.execute("""
CREATE TABLE IF NOT EXISTS evaluasi_anggaran (
    id INT AUTO_INCREMENT PRIMARY KEY,

    kode_akun VARCHAR(30) NOT NULL,
    nama_akun VARCHAR(150) NOT NULL,

    kelompok ENUM(
        'Pendapatan',
        'Belanja'
    ) NOT NULL,

    tahun_ajaran VARCHAR(20) NOT NULL,

    pagu DECIMAL(18,2) DEFAULT 0,

    q1 DECIMAL(18,2) DEFAULT 0,
    q2 DECIMAL(18,2) DEFAULT 0,
    q3 DECIMAL(18,2) DEFAULT 0,
    q4 DECIMAL(18,2) DEFAULT 0,

    total_realisasi DECIMAL(18,2) DEFAULT 0,
    sisa_surplus DECIMAL(18,2) DEFAULT 0,
    forecast DECIMAL(18,2) DEFAULT 0,
    persentase DECIMAL(10,2) DEFAULT 0,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP
)
""")
    
    cursor.execute("""
CREATE TABLE IF NOT EXISTS akun_budgeting (
    id INT AUTO_INCREMENT PRIMARY KEY,

    kode VARCHAR(30) NOT NULL UNIQUE,

    nama VARCHAR(150) NOT NULL,

    kelompok VARCHAR(100) NOT NULL,

    golongan ENUM(
        'Pendapatan',
        'Beban',
        'Aset'
    ) NOT NULL,

    keterangan TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    INDEX idx_kode (kode),
    INDEX idx_kelompok (kelompok),
    INDEX idx_golongan (golongan)

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
""")
    
    cursor.execute("""
CREATE TABLE IF NOT EXISTS akun_keuangan (
    id INT AUTO_INCREMENT PRIMARY KEY,

    kode VARCHAR(30) NOT NULL UNIQUE,

    nama VARCHAR(150) NOT NULL,

    kelompok VARCHAR(150) NOT NULL,

    golongan ENUM(
        'Aset',
        'Pendapatan',
        'Beban',
        'Liabilitas'
    ) NOT NULL,

    budgeting VARCHAR(150),

    arus_kas ENUM(
        'Operasi',
        'Investasi',
        'Pendanaan'
    ),

    keterangan TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    INDEX idx_kode (kode),
    INDEX idx_golongan (golongan),
    INDEX idx_kelompok (kelompok)

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
""")
) ENGINE=InnoDB
""")
    
# =====================================================
# REKAP PEMBAYARAN BULANAN SISWA
# =====================================================

    cursor.execute("""
CREATE TABLE IF NOT EXISTS rekap_pembayaran (

    id INT AUTO_INCREMENT PRIMARY KEY,

    nis VARCHAR(30) NOT NULL,

    nama VARCHAR(100) NOT NULL,

    kelas VARCHAR(50) NOT NULL DEFAULT '',

    tahun VARCHAR(20) NOT NULL,

    tipe VARCHAR(50) NOT NULL DEFAULT '',

    jenis VARCHAR(100) NOT NULL,

    -- Status pembayaran per bulan
    jan VARCHAR(20) DEFAULT 'Belum',
    feb VARCHAR(20) DEFAULT 'Belum',
    mar VARCHAR(20) DEFAULT 'Belum',
    apr VARCHAR(20) DEFAULT 'Belum',
    mei VARCHAR(20) DEFAULT 'Belum',
    jun VARCHAR(20) DEFAULT 'Belum',
    jul VARCHAR(20) DEFAULT 'Belum',
    ags VARCHAR(20) DEFAULT 'Belum',
    sep VARCHAR(20) DEFAULT 'Belum',
    okt VARCHAR(20) DEFAULT 'Belum',
    nov VARCHAR(20) DEFAULT 'Belum',
    des VARCHAR(20) DEFAULT 'Belum',

    created_at TIMESTAMP
    DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP
    DEFAULT CURRENT_TIMESTAMP
    ON UPDATE CURRENT_TIMESTAMP

) ENGINE=InnoDB
""")

    # =====================================================
    # REKAP PEMBAYARAN PER TANGGAL (HARIAN)
    # =====================================================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS rekap_per_tanggal (
        id INT AUTO_INCREMENT PRIMARY KEY,
        tanggal DATE NOT NULL,
        no_kwitansi VARCHAR(50) NOT NULL,
        nis VARCHAR(30) NOT NULL,
        nama VARCHAR(100) NOT NULL,
        kelas VARCHAR(50) NOT NULL,
        petugas VARCHAR(100) NOT NULL,
        nominal BIGINT NOT NULL DEFAULT 0,
        
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    ) ENGINE=InnoDB
    """)
    
    # =====================================================
    # TRANSAKSI PENGELUARAN (DIBUTUHKAN OLEH LAPORAN PENERIMAAN)
    # =====================================================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transaksi_pengeluaran (
        id INT AUTO_INCREMENT PRIMARY KEY,
        kode VARCHAR(50) NOT NULL,
        tanggal DATE NOT NULL,
        jenis VARCHAR(100) NOT NULL,
        sumber VARCHAR(150) NOT NULL,
        petugas VARCHAR(100) NOT NULL,
        menyetujui VARCHAR(100) NOT NULL,
        keterangan TEXT DEFAULT NULL,
        nominal BIGINT NOT NULL DEFAULT 0,
        
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    ) ENGINE=InnoDB
    """)
