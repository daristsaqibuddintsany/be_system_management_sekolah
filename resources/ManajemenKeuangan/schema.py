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

        tipe ENUM(
            'Bebas',
            'Wajib'
        ) DEFAULT 'Wajib',

        status ENUM(
            'aktif',
            'nonaktif'
        ) DEFAULT 'aktif',

        created_at TIMESTAMP
        DEFAULT CURRENT_TIMESTAMP,

        updated_at TIMESTAMP
        DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP

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

        created_at TIMESTAMP
        DEFAULT CURRENT_TIMESTAMP,

        updated_at TIMESTAMP
        DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP

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

        metode_pembayaran VARCHAR(50)
        DEFAULT 'cash',

        keterangan TEXT DEFAULT NULL,

        status ENUM(
            'lunas',
            'cicil',
            'belum',
            'aktif'
        ) DEFAULT 'belum',

        tanggal_bayar DATE DEFAULT NULL,

        created_at TIMESTAMP
        DEFAULT CURRENT_TIMESTAMP,

        updated_at TIMESTAMP
        DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

        CONSTRAINT fk_pembayaran_jenis
        FOREIGN KEY (jenis_pembayaran_id)
        REFERENCES jenis_pembayaran(id)
        ON DELETE SET NULL

    ) ENGINE=InnoDB
    """)

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

        status ENUM(
            'lunas',
            'belum_lunas'
        ) DEFAULT 'belum_lunas',

        keterangan TEXT DEFAULT NULL,

        created_at TIMESTAMP
        DEFAULT CURRENT_TIMESTAMP,

        updated_at TIMESTAMP
        DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP

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

        SUM(
            p.jumlah_tagihan
        ) AS total_tagihan,

        SUM(
            p.jumlah_bayar
        ) AS total_bayar,

        SUM(
            p.sisa_tagihan
        ) AS total_tunggakan

    FROM pembayaran p

    GROUP BY

        p.siswa_id,
        p.nis,
        p.nama_siswa,
        p.kelas,
        p.tahun_ajaran
    """)
    
    cursor.execute("""
CREATE TABLE IF NOT EXISTS transaksi_tabungan_teller (

    id INT AUTO_INCREMENT PRIMARY KEY,

    nis VARCHAR(30) NOT NULL,

    jenis ENUM(
        'Penyetoran',
        'Penarikan'
    ) NOT NULL,

    nominal BIGINT NOT NULL DEFAULT 0,

    keterangan TEXT DEFAULT NULL,

    created_at TIMESTAMP
    DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP
    DEFAULT CURRENT_TIMESTAMP
    ON UPDATE CURRENT_TIMESTAMP

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

    created_at TIMESTAMP
    DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP
    DEFAULT CURRENT_TIMESTAMP
    ON UPDATE CURRENT_TIMESTAMP

) ENGINE=InnoDB
""")
    
    cursor.execute("""
CREATE TABLE IF NOT EXISTS riwayat_tabungan (

    id INT AUTO_INCREMENT PRIMARY KEY,

    transaksi_id INT DEFAULT NULL,

    nis VARCHAR(30) NOT NULL,

    nama_siswa VARCHAR(100) DEFAULT NULL,

    jenis ENUM(
        'Setor',
        'Tarik'
    ) NOT NULL,

    jumlah BIGINT NOT NULL DEFAULT 0,

    keterangan TEXT DEFAULT NULL,

    tanggal DATE NOT NULL,

    created_at TIMESTAMP
    DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_riwayat_tabungan
    FOREIGN KEY (transaksi_id)
    REFERENCES transaksi_tabungan_teller(id)
    ON DELETE CASCADE

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

    created_at TIMESTAMP
    DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_riwayat_transaksi
    FOREIGN KEY (transaksi_id)
    REFERENCES transaksi_tabungan_teller(id)
    ON DELETE CASCADE

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

    status ENUM(
        'Aktif',
        'Nonaktif'
    ) DEFAULT 'Aktif',

    created_at TIMESTAMP
    DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP
    DEFAULT CURRENT_TIMESTAMP
    ON UPDATE CURRENT_TIMESTAMP

) ENGINE=InnoDB
""")
    
    # =========================
# TABEL TRANSAKSI PENGELUARAN
# =========================

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

    nominal DECIMAL(15,2) DEFAULT 0,

    created_at TIMESTAMP
    DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP
    DEFAULT CURRENT_TIMESTAMP
    ON UPDATE CURRENT_TIMESTAMP

) ENGINE=InnoDB
""")
    