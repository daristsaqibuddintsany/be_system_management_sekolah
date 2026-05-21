from models.connection import get_connection

from resources.ManajemenUser.schema import create_users_table
from resources.ManajemenSiswa.schema import create_siswa_tables
from resources.ManajemenGuru.schema import create_guru_table


def init_db():

    conn = get_connection()
    cursor = conn.cursor()

    create_users_table(cursor)

    create_siswa_tables(cursor)
    
    create_guru_table(cursor)

    conn.commit()

    cursor.close()
    conn.close()