from models.connection import get_connection

from resources.ManajemenUser.schema import create_users_table
from resources.ManajemenSiswa.schema import create_siswa_tables


def init_db():

    conn = get_connection()
    cursor = conn.cursor()

    create_users_table(cursor)

    create_siswa_tables(cursor)

    conn.commit()

    cursor.close()
    conn.close()