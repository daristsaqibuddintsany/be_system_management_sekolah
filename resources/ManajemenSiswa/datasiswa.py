import os
import uuid
import falcon
import traceback

from models.connection import get_connection


# ====================================
# CONFIG UPLOAD
# ====================================

BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../../"
    )
)

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ====================================
# PARSER MULTIPART (FIX)
# ====================================

def parse_media(req):

    form = req.get_media()
    data = {}

    for part in form:

        # nama field
        field_name = part.name

        # ======================
        # FILE
        # ======================

        if part.filename:

            data[field_name] = part

        # ======================
        # TEXT
        # ======================

        else:

            data[field_name] = part.text

    return data


# ====================================
# SISWA RESOURCE
# ====================================

class SiswaResource:

    # ====================================
    # GET ALL
    # ====================================

    def on_get(self, req, resp):

        try:

            conn = get_connection()
            cursor = conn.cursor(dictionary=True)

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

    # ====================================
    # CREATE
    # ====================================

    def on_post(self, req, resp):

        try:

            media = parse_media(req)

            nis = media.get("nis")
            nama = media.get("nama")

            # VALIDASI
            if not nis or not nama:

                resp.status = falcon.HTTP_400
                resp.media = {
                    "status": False,
                    "message": "NIS dan Nama wajib diisi"
                }
                return

            # ====================================
            # HANDLE FOTO
            # ====================================

            foto = media.get("foto")
            foto_filename = None

            if foto and hasattr(foto, "filename"):

                ext = foto.filename.split(".")[-1]

                foto_filename = f"{uuid.uuid4()}.{ext}"

                save_path = os.path.join(
                    UPLOAD_FOLDER,
                    foto_filename
                )

                with open(save_path, "wb") as f:

                    f.write(foto.file.read())

            # ====================================
            # INSERT DATABASE
            # ====================================

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
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
                    %s,%s,%s,%s,
                    %s,%s,%s,
                    %s,%s,%s,%s
                )
            """, (

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

            ))

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


# ====================================
# SISWA BY ID
# ====================================

class SiswaByIdResource:

    # ====================================
    # GET BY ID
    # ====================================

    def on_get(self, req, resp, id):

        try:

            conn = get_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute("""
                SELECT *
                FROM siswa
                WHERE id = %s
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

    # ====================================
    # UPDATE
    # ====================================

    def on_put(self, req, resp, id):

        try:

            media = parse_media(req)

            conn = get_connection()
            cursor = conn.cursor(dictionary=True)

            # ambil foto lama
            cursor.execute(
                "SELECT foto FROM siswa WHERE id=%s",
                (id,)
            )

            old = cursor.fetchone()

            foto_filename = old["foto"] if old else None

            # ====================================
            # HANDLE FOTO BARU
            # ====================================

            foto = media.get("foto")

            if foto and hasattr(foto, "filename"):

                # hapus foto lama
                if foto_filename:

                    old_path = os.path.join(
                        UPLOAD_FOLDER,
                        foto_filename
                    )

                    if os.path.exists(old_path):

                        os.remove(old_path)

                # simpan foto baru
                ext = foto.filename.split(".")[-1]

                foto_filename = f"{uuid.uuid4()}.{ext}"

                save_path = os.path.join(
                    UPLOAD_FOLDER,
                    foto_filename
                )

                with open(save_path, "wb") as f:

                    f.write(foto.file.read())

            # ====================================
            # UPDATE DB
            # ====================================

            cursor.execute("""
                UPDATE siswa SET
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
            """, (

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

            ))

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

    # ====================================
    # DELETE
    # ====================================

    def on_delete(self, req, resp, id):

        try:

            conn = get_connection()
            cursor = conn.cursor(dictionary=True)

            # ambil foto
            cursor.execute(
                "SELECT foto FROM siswa WHERE id=%s",
                (id,)
            )

            data = cursor.fetchone()

            # hapus file foto
            if data and data["foto"]:

                foto_path = os.path.join(
                    UPLOAD_FOLDER,
                    data["foto"]
                )

                if os.path.exists(foto_path):

                    os.remove(foto_path)

            # hapus db
            cursor.execute(
                "DELETE FROM siswa WHERE id=%s",
                (id,)
            )

            conn.commit()

            cursor.close()
            conn.close()

            resp.media = {
                "status": True,
                "message": "Data siswa berhasil dihapus"
            }

        except Exception as e:

            traceback.print_exc()

            resp.status = falcon.HTTP_500

            resp.media = {
                "status": False,
                "message": str(e)
            }