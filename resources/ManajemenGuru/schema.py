def create_guru_table(cursor):

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS jadwal_mengajar (

        id INT AUTO_INCREMENT PRIMARY KEY,

        nama_guru VARCHAR(100) NOT NULL,

        mata_pelajaran VARCHAR(100) NOT NULL,

        kelas VARCHAR(50) NOT NULL,

        hari VARCHAR(30) NOT NULL,

        jam_mulai TIME NOT NULL,

        jam_selesai TIME NOT NULL,

        tahun_ajaran VARCHAR(20) NOT NULL

    )
    """)
    
    cursor.execute("""
CREATE TABLE IF NOT EXISTS mata_pelajaran (

    id INT AUTO_INCREMENT PRIMARY KEY,

    nama VARCHAR(100) NOT NULL

)
""")