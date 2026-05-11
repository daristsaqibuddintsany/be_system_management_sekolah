from models.schema import get_connection
import falcon


class SiswaResource:

    # =========================
    # GET DATA SISWA
    # =========================
    def on_get(self, req, resp):

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT * FROM siswa
            ORDER BY id DESC
        """)

        data = cursor.fetchall()

        cursor.close()
        conn.close()

        resp.media = data


    # =========================
    # TAMBAH SISWA
    # =========================
    def on_post(self, req, resp):

        try:

            body = req.media

            if not body.get("nis") or not body.get("nama"):

                resp.status = falcon.HTTP_400

                resp.media = {
                    "status": False,
                    "message": "NIS dan Nama wajib diisi"
                }

                return

            conn = get_connection()
            cursor = conn.cursor()

            query = """
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
                hubungan_wali
            )
            VALUES (
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s
            )
            """

            values = (
                body.get("nis"),
                body.get("nisn"),
                body.get("nama"),
                body.get("tempat_lahir"),
                body.get("tanggal_lahir"),
                body.get("jenis_kelamin"),
                body.get("alamat"),
                body.get("agama"),
                body.get("golongan_darah"),
                body.get("status"),
                body.get("tahun_ajaran"),
                body.get("tahun_masuk"),
                body.get("kelas"),
                body.get("jurusan"),
                body.get("no_hp"),
                body.get("sekolah_asal"),
                body.get("ayah"),
                body.get("pekerjaan_ayah"),
                body.get("hp_ayah"),
                body.get("ibu"),
                body.get("pekerjaan_ibu"),
                body.get("hp_ibu"),
                body.get("wali"),
                body.get("hp_wali"),
                body.get("hubungan_wali")
            )

            cursor.execute(query, values)

            conn.commit()

            cursor.close()
            conn.close()

            resp.media = {
                "status": True,
                "message": "Data siswa berhasil ditambahkan"
            }

        except Exception as e:

            resp.status = falcon.HTTP_500

            resp.media = {
                "status": False,
                "message": str(e)
            }