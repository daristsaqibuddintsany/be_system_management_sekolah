def create_guru_table(cursor):

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS guru (

        id INT AUTO_INCREMENT PRIMARY KEY,

        nip VARCHAR(50) UNIQUE,

        nama_guru VARCHAR(100) NOT NULL,

        jenis_kelamin ENUM(
            'Laki-laki',
            'Perempuan'
        ) NOT NULL,

        tempat_lahir VARCHAR(100),

        tanggal_lahir DATE,

        alamat TEXT,

        no_hp VARCHAR(20),

        email VARCHAR(100),

        pendidikan_terakhir VARCHAR(100),

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