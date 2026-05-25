def create_guru_table(cursor):

    # =====================================================
    # MATA PELAJARAN (Dibutuhkan oleh matapelajaran.py)
    # =====================================================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS mata_pelajaran (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nama VARCHAR(150) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    ) ENGINE=InnoDB
    """)

    # =====================================================
    # JADWAL MENGAJAR (Dibutuhkan oleh jadwalmengajar.py)
    # =====================================================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS jadwal_mengajar (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nama_guru VARCHAR(100) NOT NULL,
        mata_pelajaran VARCHAR(150) NOT NULL,
        kelas VARCHAR(50) NOT NULL,
        hari VARCHAR(20) NOT NULL,
        jam_mulai TIME NOT NULL,
        jam_selesai TIME NOT NULL,
        tahun_ajaran VARCHAR(20) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    ) ENGINE=InnoDB
    """)