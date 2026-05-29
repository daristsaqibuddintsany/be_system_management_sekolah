def create_aplikasi_table(cursor):
    
    # =====================================================
# MANAJEMEN USER
# =====================================================

    cursor.execute("""
CREATE TABLE IF NOT EXISTS manajemen_user (

    id INT AUTO_INCREMENT PRIMARY KEY,

    jenis_user ENUM(
        'Siswa',
        'Guru',
        'Wali Kelas',
        'Orang Tua'
    ) NOT NULL,

    nis_id VARCHAR(100) UNIQUE NOT NULL,

    nama VARCHAR(150) NOT NULL,

    kelas VARCHAR(50),

    password VARCHAR(255),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ON UPDATE CURRENT_TIMESTAMP

) ENGINE=InnoDB
""")
    
    cursor.execute("""
CREATE TABLE IF NOT EXISTS informasi_lembaga (

    id INT AUTO_INCREMENT PRIMARY KEY,

    judul VARCHAR(255) NOT NULL,

    isi TEXT NOT NULL,

    tanggal DATE NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ON UPDATE CURRENT_TIMESTAMP

) ENGINE=InnoDB
""")
    
    cursor.execute("""
CREATE TABLE IF NOT EXISTS backup_data (

    id INT AUTO_INCREMENT PRIMARY KEY,

    nama_file VARCHAR(255) NOT NULL,

    path_file TEXT NOT NULL,

    tipe ENUM('partial', 'full') DEFAULT 'partial',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

) ENGINE=InnoDB
""")
    
    cursor.execute("""
CREATE TABLE IF NOT EXISTS setting_gps (
    id INT AUTO_INCREMENT PRIMARY KEY,

    nama VARCHAR(150) NOT NULL,

    latitude VARCHAR(50) NOT NULL,
    longitude VARCHAR(50) NOT NULL,

    radius INT NOT NULL,

    jam_masuk TIME NOT NULL,
    jam_selesai TIME NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP

) ENGINE=InnoDB
""")
    
    cursor.execute("""
CREATE TABLE IF NOT EXISTS banner_aplikasi (

    id INT AUTO_INCREMENT PRIMARY KEY,

    nama_file VARCHAR(255) NOT NULL,

    path_file TEXT NOT NULL,

    preview_url TEXT,

    diunggah TIMESTAMP DEFAULT CURRENT_TIMESTAMP

) ENGINE=InnoDB
""")