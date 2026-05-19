def create_siswa_tables(cursor):

    # =========================
    # SISWA
    # =========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS siswa (

        id INT AUTO_INCREMENT PRIMARY KEY,

        nis VARCHAR(50) NOT NULL,

        nisn VARCHAR(50),

        nama VARCHAR(100) NOT NULL,

        tempat_lahir VARCHAR(100),

        tanggal_lahir DATE,

        jenis_kelamin VARCHAR(20),

        alamat TEXT,

        agama VARCHAR(50),

        golongan_darah VARCHAR(10),

        status VARCHAR(20),

        tahun_ajaran VARCHAR(20),

        tahun_masuk VARCHAR(20),

        kelas VARCHAR(50),

        jurusan VARCHAR(50),

        no_hp VARCHAR(20),

        sekolah_asal VARCHAR(100),

        ayah VARCHAR(100),

        pekerjaan_ayah VARCHAR(100),

        hp_ayah VARCHAR(20),

        ibu VARCHAR(100),

        pekerjaan_ibu VARCHAR(100),

        hp_ibu VARCHAR(20),

        wali VARCHAR(100),

        hp_wali VARCHAR(20),

        hubungan_wali VARCHAR(50)

    )
    """)

    # =========================
    # DATA KELAS
    # =========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS data_kelas (

        id INT AUTO_INCREMENT PRIMARY KEY,

        kelas VARCHAR(100) NOT NULL,

        jurusan VARCHAR(100) NOT NULL

    )
    """)

    # =========================
    # DATA JURUSAN
    # =========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS data_jurusan (

        id INT AUTO_INCREMENT PRIMARY KEY,

        kode VARCHAR(50) NOT NULL,

        nama VARCHAR(100) NOT NULL

    )
    """)

    # =========================
    # ASPEK PENILAIAN
    # =========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS aspek_penilaian (

        id INT AUTO_INCREMENT PRIMARY KEY,

        nama VARCHAR(100) NOT NULL,

        keterangan TEXT,

        editable BOOLEAN DEFAULT TRUE

    )
    """)

    # =========================
    # EXTRACURRICULAR
    # =========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS extracurricular (

        id INT AUTO_INCREMENT PRIMARY KEY,

        nama VARCHAR(100) NOT NULL,

        pembina VARCHAR(100),

        jadwal VARCHAR(100),

        keterangan TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)
    
    
    cursor.execute("""
CREATE TABLE IF NOT EXISTS jenis_semester (

    id INT AUTO_INCREMENT PRIMARY KEY,

    nama VARCHAR(150) NOT NULL

)
""")