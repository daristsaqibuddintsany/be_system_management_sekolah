def create_users_table(cursor):

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (

        id INT AUTO_INCREMENT PRIMARY KEY,

        nama VARCHAR(100) NOT NULL,

        email VARCHAR(100) UNIQUE NOT NULL,

        password VARCHAR(255) NOT NULL

    )
    """)