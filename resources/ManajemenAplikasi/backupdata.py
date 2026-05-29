import falcon
import os
from datetime import datetime

from models.connection import get_connection


class BackupDataResource:

    # =========================
    # GET LIST BACKUP FILE
    # =========================
    def on_get(self, req, resp):

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
        SELECT *
        FROM backup_data
        ORDER BY id DESC
        """)

        data = cursor.fetchall()

        cursor.close()
        conn.close()

        resp.media = data

    # =========================
    # CREATE BACKUP (SIMULASI SQL EXPORT)
    # =========================
    def on_post(self, req, resp):

        conn = get_connection()
        cursor = conn.cursor()

        # nama file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"backup_partial__{timestamp}.sql"

        backup_dir = "backups"

        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

        file_path = os.path.join(backup_dir, filename)

        # =========================
        # SIMULASI DUMP SQL
        # =========================
        with open(file_path, "w", encoding="utf-8") as f:

            # contoh backup tabel penting (partial)
            tables = [
                "data_buku",
                "peminjaman_buku",
                "pengembalian_buku",
                "manajemen_user"
            ]

            for table in tables:

                cursor.execute(f"SELECT * FROM {table}")
                rows = cursor.fetchall()

                f.write(f"-- BACKUP TABLE {table}\n")

                for row in rows:
                    values = ",".join(
                        [f"'{str(v)}'" for v in row.values()]
                    )

                    f.write(
                        f"INSERT INTO {table} VALUES ({values});\n"
                    )

                f.write("\n")

        # =========================
        # SIMPAN KE DATABASE
        # =========================

        cursor.execute("""
        INSERT INTO backup_data (
            nama_file,
            path_file,
            tipe
        ) VALUES (%s, %s, %s)
        """, (
            filename,
            file_path,
            "partial"
        ))

        conn.commit()

        cursor.close()
        conn.close()

        resp.media = {
            "message": "Backup berhasil dibuat",
            "file": filename
        }