import falcon
from models.connection import get_connection

class JenisPengeluaranResource:

    # =========================
    # GET ALL JENIS PENGELUARAN
    # =========================
    def on_get(self, req, resp):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT id, kode_keuangan, kode_pengeluaran, nama, jenis, keterangan, status 
            FROM jenis_pengeluaran 
            ORDER BY id DESC
        """)
        data = cursor.fetchall()

        # Mapping key database (snake_case) ke format frontend (camelCase)
        formatted_data = []
        for row in data:
            formatted_data.append({
                "id": row["id"],
                "kodeKeuangan": row["kode_keuangan"],
                "kodePengeluaran": row["kode_pengeluaran"],
                "nama": row["nama"],
                "jenis": row["jenis"],
                "keterangan": row["keterangan"],
                "status": row["status"]
            })

        cursor.close()
        conn.close()

        resp.media = formatted_data
        resp.status = falcon.HTTP_200

    # =========================
    # CREATE JENIS PENGELUARAN
    # =========================
    def on_post(self, req, resp):
        body = req.media or {}

        # Validasi field wajib sesuai handle handleSubmit di React
        if (not body.get("kodeKeuangan") or not body.get("kodePengeluaran") or 
            not body.get("nama") or not body.get("jenis") or not body.get("status")):
            raise falcon.HTTPBadRequest(
                title="Missing fields",
                description="Semua field (kecuali keterangan) wajib diisi!"
            )

        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO jenis_pengeluaran (
                    kode_keuangan, kode_pengeluaran, nama, jenis, keterangan, status
                ) VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                body.get("kodeKeuangan"),
                body.get("kodePengeluaran"),
                body.get("nama"),
                body.get("jenis"),
                body.get("keterangan"),
                body.get("status")
            ))
            conn.commit()
            
            resp.media = {"message": "Data berhasil ditambahkan"}
            resp.status = falcon.HTTP_201
            
        except Exception as e:
            raise falcon.HTTPBadRequest(title="Database Error", description=str(e))
        finally:
            cursor.close()
            conn.close()


class JenisPengeluaranByIdResource:

    # =========================
    # UPDATE JENIS PENGELUARAN
    # =========================
    def on_put(self, req, resp, id):
        body = req.media or {}

        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                UPDATE jenis_pengeluaran
                SET
                    kode_keuangan=%s,
                    kode_pengeluaran=%s,
                    nama=%s,
                    jenis=%s,
                    keterangan=%s,
                    status=%s
                WHERE id=%s
            """, (
                body.get("kodeKeuangan"),
                body.get("kodePengeluaran"),
                body.get("nama"),
                body.get("jenis"),
                body.get("keterangan"),
                body.get("status"),
                id
            ))
            conn.commit()

            resp.media = {"message": "Data berhasil diupdate"}
            resp.status = falcon.HTTP_200
            
        except Exception as e:
            raise falcon.HTTPBadRequest(title="Database Error", description=str(e))
        finally:
            cursor.close()
            conn.close()

    # =========================
    # DELETE JENIS PENGELUARAN
    # =========================
    def on_delete(self, req, resp, id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM jenis_pengeluaran WHERE id=%s", (id,))
        conn.commit()
        
        cursor.close()
        conn.close()

        resp.media = {"message": "Data berhasil dihapus"}
        resp.status = falcon.HTTP_200