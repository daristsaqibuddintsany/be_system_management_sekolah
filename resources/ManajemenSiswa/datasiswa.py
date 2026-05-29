import os
import uuid
import falcon
import traceback

from models.connection import get_connection

# =========================================
# ROOT PROJECT
# =========================================

ROOT_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

# =========================================
# UPLOAD FOLDER
# =========================================

UPLOAD_FOLDER = os.path.join(
    ROOT_DIR,
    "uploads"
)

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

print("📂 UPLOAD FOLDER:", UPLOAD_FOLDER)

# =========================================
# PARSE MULTIPART
# =========================================

def parse_media(req):

    form = req.get_media()

    data = {}

    for part in form:

        # FILE
        if getattr(part, "filename", None):

            data[part.name] = part

        # TEXT
        else:

            data[part.name] = part.text

    return data

# =========================================
# SAVE FOTO
# =========================================

def save_foto(foto):

    if not foto:

        return None

    try:

        original_filename = foto.filename

        ext = original_filename.split(".")[-1].lower()

        new_filename = f"{uuid.uuid4()}.{ext}"

        filepath = os.path.join(
            UPLOAD_FOLDER,
            new_filename
        )

        file_data = foto.stream.read()

        if not file_data:

            return None

        with open(filepath, "wb") as f:

            f.write(file_data)

        print("✅ FOTO DISIMPAN:", filepath)

        return new_filename

    except Exception as e:

        print("❌ ERROR SAVE FOTO:", str(e))

        traceback.print_exc()

        return None

# =========================================
# SISWA RESOURCE
# =========================================

class SiswaResource:

    # =====================================
    # GET ALL
    # =====================================

    def on_get(self, req, resp):

        try:

            conn = get_connection()

            cursor = conn.cursor(
                dictionary=True
            )

            cursor.execute("""
                SELECT *
                FROM siswa
                ORDER BY id DESC
            """)

            data = cursor.fetchall()

            cursor.close()
            conn.close()

            resp.media = data

        except Exception as e:

            traceback.print_exc()

            resp.status = falcon.HTTP_500

            resp.media = {
                "status": False,
                "message": str(e)
            }

    # =====================================
    # POST
    # =====================================

    def on_post(self, req, resp):

        try:

            media = parse_media(req)

            foto = media.get("foto")

            foto_filename = save_foto(foto)

            conn = get_connection()

            cursor = conn.cursor()

            sql = """
                INSERT INTO siswa (
                    nis,
                    nisn,
                    nama,
                    tempat_lahir,
                    tanggal_lahir,
                    jenis_kelamin,
                    alamat,
                    agama,
                    golongan_darah,
                    status,
                    tahun_ajaran,
                    tahun_masuk,
                    kelas,
                    jurusan,
                    no_hp,
                    sekolah_asal,
                    ayah,
                    pekerjaan_ayah,
                    hp_ayah,
                    ibu,
                    pekerjaan_ibu,
                    hp_ibu,
                    wali,
                    hp_wali,
                    hubungan_wali,
                    foto
                )
                VALUES (
                    %s,%s,%s,%s,%s,
                    %s,%s,%s,%s,%s,
                    %s,%s,%s,%s,%s,
                    %s,%s,%s,%s,%s,
                    %s,%s,%s,%s,%s,
                    %s
                )
            """

            values = (

                media.get("nis"),
                media.get("nisn"),
                media.get("nama"),
                media.get("tempat_lahir"),
                media.get("tanggal_lahir"),
                media.get("jenis_kelamin"),
                media.get("alamat"),
                media.get("agama"),
                media.get("golongan_darah"),
                media.get("status"),
                media.get("tahun_ajaran"),
                media.get("tahun_masuk"),
                media.get("kelas"),
                media.get("jurusan"),
                media.get("no_hp"),
                media.get("sekolah_asal"),
                media.get("ayah"),
                media.get("pekerjaan_ayah"),
                media.get("hp_ayah"),
                media.get("ibu"),
                media.get("pekerjaan_ibu"),
                media.get("hp_ibu"),
                media.get("wali"),
                media.get("hp_wali"),
                media.get("hubungan_wali"),
                foto_filename

            )

            cursor.execute(sql, values)

            conn.commit()

            cursor.close()
            conn.close()

            resp.media = {
                "status": True,
                "message": "Data siswa berhasil ditambahkan"
            }

        except Exception as e:

            traceback.print_exc()

            resp.status = falcon.HTTP_500

            resp.media = {
                "status": False,
                "message": str(e)
            }

# =========================================
# SISWA BY ID
# =========================================

class SiswaByIdResource:

    # =====================================
    # GET BY ID
    # =====================================

    def on_get(self, req, resp, id):

        try:

            conn = get_connection()

            cursor = conn.cursor(
                dictionary=True
            )

            cursor.execute("""
                SELECT *
                FROM siswa
                WHERE id=%s
            """, (id,))

            data = cursor.fetchone()

            cursor.close()
            conn.close()

            if not data:

                resp.status = falcon.HTTP_404

                resp.media = {
                    "status": False,
                    "message": "Data tidak ditemukan"
                }

                return

            resp.media = data

        except Exception as e:

            traceback.print_exc()

            resp.status = falcon.HTTP_500

            resp.media = {
                "status": False,
                "message": str(e)
            }

    # =====================================
    # UPDATE
    # =====================================

    def on_put(self, req, resp, id):

        try:

            media = parse_media(req)

            conn = get_connection()

            cursor = conn.cursor(
                dictionary=True
            )

            # =========================
            # CEK DATA LAMA
            # =========================

            cursor.execute(
                "SELECT foto FROM siswa WHERE id=%s",
                (id,)
            )

            old_data = cursor.fetchone()

            if not old_data:

                resp.status = falcon.HTTP_404

                resp.media = {
                    "status": False,
                    "message": "Data tidak ditemukan"
                }

                return

            # =========================
            # FOTO
            # =========================

            foto_filename = old_data["foto"]

            foto = media.get("foto")

            if foto:

                # hapus foto lama
                if foto_filename:

                    old_path = os.path.join(
                        UPLOAD_FOLDER,
                        foto_filename
                    )

                    if os.path.exists(old_path):

                        os.remove(old_path)

                        print("🗑 FOTO LAMA DIHAPUS")

                # simpan foto baru
                foto_filename = save_foto(foto)

            # =========================
            # UPDATE DB
            # =========================

            sql = """
                UPDATE siswa
                SET
                    nis=%s,
                    nisn=%s,
                    nama=%s,
                    tempat_lahir=%s,
                    tanggal_lahir=%s,
                    jenis_kelamin=%s,
                    alamat=%s,
                    agama=%s,
                    golongan_darah=%s,
                    status=%s,
                    tahun_ajaran=%s,
                    tahun_masuk=%s,
                    kelas=%s,
                    jurusan=%s,
                    no_hp=%s,
                    sekolah_asal=%s,
                    ayah=%s,
                    pekerjaan_ayah=%s,
                    hp_ayah=%s,
                    ibu=%s,
                    pekerjaan_ibu=%s,
                    hp_ibu=%s,
                    wali=%s,
                    hp_wali=%s,
                    hubungan_wali=%s,
                    foto=%s
                WHERE id=%s
            """

            values = (

                media.get("nis"),
                media.get("nisn"),
                media.get("nama"),
                media.get("tempat_lahir"),
                media.get("tanggal_lahir"),
                media.get("jenis_kelamin"),
                media.get("alamat"),
                media.get("agama"),
                media.get("golongan_darah"),
                media.get("status"),
                media.get("tahun_ajaran"),
                media.get("tahun_masuk"),
                media.get("kelas"),
                media.get("jurusan"),
                media.get("no_hp"),
                media.get("sekolah_asal"),
                media.get("ayah"),
                media.get("pekerjaan_ayah"),
                media.get("hp_ayah"),
                media.get("ibu"),
                media.get("pekerjaan_ibu"),
                media.get("hp_ibu"),
                media.get("wali"),
                media.get("hp_wali"),
                media.get("hubungan_wali"),
                foto_filename,
                id

            )

            cursor.execute(sql, values)

            conn.commit()

            cursor.close()
            conn.close()

            resp.media = {
                "status": True,
                "message": "Data siswa berhasil diupdate"
            }

        except Exception as e:

            traceback.print_exc()

            resp.status = falcon.HTTP_500

            resp.media = {
                "status": False,
                "message": str(e)
            }

    # =====================================
    # DELETE
    # =====================================

    def on_delete(self, req, resp, id):

        try:

            conn = get_connection()

            cursor = conn.cursor(
                dictionary=True
            )

            # =========================
            # AMBIL FOTO
            # =========================

            cursor.execute(
                "SELECT foto FROM siswa WHERE id=%s",
                (id,)
            )

            data = cursor.fetchone()

            # =========================
            # HAPUS FOTO
            # =========================

            if data and data["foto"]:

                foto_path = os.path.join(
                    UPLOAD_FOLDER,
                    data["foto"]
                )

                if os.path.exists(foto_path):

                    os.remove(foto_path)

                    print("🗑 FOTO DIHAPUS")

            # =========================
            # HAPUS DB
            # =========================

            cursor.execute(
                "DELETE FROM siswa WHERE id=%s",
                (id,)
            )

            conn.commit()

            cursor.close()
            conn.close()

            resp.media = {
                "status": True,
                "message": "Data berhasil dihapus"
            }

        except Exception as e:

            traceback.print_exc()

            resp.status = falcon.HTTP_500

            resp.media = {
                "status": False,
                "message": str(e)
            }