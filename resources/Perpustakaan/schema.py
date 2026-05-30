
def create_perpustakaan_table(cursor):

    # =====================================================
    # DATA BUKU
    # =====================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS data_buku (

        id INT AUTO_INCREMENT PRIMARY KEY,

        barcode VARCHAR(50) NOT NULL UNIQUE,

        judul VARCHAR(200) NOT NULL,

        isbn VARCHAR(100),

        penulis VARCHAR(150),

        penerbit VARCHAR(150),

        tahun YEAR,

        harga BIGINT DEFAULT 0,

        kondisi ENUM(
            'Baik',
            'Rusak Ringan',
            'Rusak Berat',
            'Tidak Diketahui'
        ) DEFAULT 'Baik',

        kategori VARCHAR(100),

        rak VARCHAR(100),

        stok INT DEFAULT 0,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

        INDEX idx_judul (judul),
        INDEX idx_isbn (isbn),
        INDEX idx_kategori (kategori),
        INDEX idx_rak (rak)

    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    # =====================================================
    # PEMINJAMAN
    # =====================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS peminjaman_buku (

        id INT AUTO_INCREMENT PRIMARY KEY,

        kode_peminjaman VARCHAR(50) NOT NULL UNIQUE,

        anggota_id INT NOT NULL,

        nama_anggota VARCHAR(150) NOT NULL,

        tanggal_pinjam DATE NOT NULL,

        tanggal_kembali DATE NOT NULL,

        total_buku INT DEFAULT 0,

        status ENUM(
            'Dipinjam',
            'Dikembalikan',
            'Terlambat'
        ) DEFAULT 'Dipinjam',

        catatan TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

        INDEX idx_kode (kode_peminjaman),
        INDEX idx_anggota (anggota_id),
        INDEX idx_status (status)

    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    # =====================================================
    # DETAIL PEMINJAMAN
    # =====================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS peminjaman_buku_detail (

        id INT AUTO_INCREMENT PRIMARY KEY,

        peminjaman_id INT NOT NULL,

        buku_id INT NOT NULL,

        barcode VARCHAR(50),

        judul_buku VARCHAR(200) NOT NULL,

        qty INT DEFAULT 1,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY (peminjaman_id)
        REFERENCES peminjaman_buku(id)
        ON DELETE CASCADE,

        FOREIGN KEY (buku_id)
        REFERENCES data_buku(id)
        ON DELETE CASCADE,

        INDEX idx_peminjaman (peminjaman_id),
        INDEX idx_buku (buku_id)

    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    # =====================================================
    # PENGEMBALIAN
    # =====================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pengembalian_buku (

        id INT AUTO_INCREMENT PRIMARY KEY,

        peminjaman_id INT NOT NULL,

        kode_pengembalian VARCHAR(50) UNIQUE NOT NULL,

        kode_peminjaman VARCHAR(50) NOT NULL,

        anggota_id INT NOT NULL,

        nama_anggota VARCHAR(150) NOT NULL,

        tanggal_pinjam DATE NOT NULL,

        tanggal_kembali DATE NOT NULL,

        tanggal_dikembalikan DATE NOT NULL,

        total_buku INT DEFAULT 0,

        total_denda BIGINT DEFAULT 0,

        status ENUM(
            'Dikembalikan',
            'Terlambat'
        ) DEFAULT 'Dikembalikan',

        catatan TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

        FOREIGN KEY (peminjaman_id)
        REFERENCES peminjaman_buku(id)
        ON DELETE CASCADE,

        INDEX idx_pengembalian (kode_pengembalian),
        INDEX idx_peminjaman (peminjaman_id)

    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    # =====================================================
    # DETAIL PENGEMBALIAN
    # =====================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pengembalian_buku_detail (

        id INT AUTO_INCREMENT PRIMARY KEY,

        pengembalian_id INT NOT NULL,

        buku_id INT NOT NULL,

        barcode VARCHAR(100),

        judul_buku VARCHAR(200) NOT NULL,

        qty INT DEFAULT 1,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY (pengembalian_id)
        REFERENCES pengembalian_buku(id)
        ON DELETE CASCADE,

        FOREIGN KEY (buku_id)
        REFERENCES data_buku(id)
        ON DELETE CASCADE

    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    # =====================================================
    # SETTING DENDA
    # =====================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS setting_denda (

        id INT AUTO_INCREMENT PRIMARY KEY,

        denda_per_hari BIGINT NOT NULL DEFAULT 1000,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP

    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    # =====================================================
    # DEFAULT DENDA
    # =====================================================

    cursor.execute("""
    SELECT COUNT(*) FROM setting_denda
    """)

    total = cursor.fetchone()[0]

    if total == 0:

        cursor.execute("""
        INSERT INTO setting_denda (
            denda_per_hari
        ) VALUES (%s)
        """, (1000,))

