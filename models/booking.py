from datetime import datetime


class Booking:

    STATUS_VALID = [
        "Menunggu",
        "Diproses",
        "Selesai",
        "Dibatalkan"
    ]

    def __init__(
        self,
        id_booking: str,
        tanggal: datetime,
        pelanggan,
        fotografer,
        paket
    ) -> None:

        self.__id_booking = id_booking
        self.tanggal = tanggal

        self.__status = "Menunggu"

        self.__pelanggan = pelanggan
        self.__fotografer = fotografer
        self.__paket = paket

    @property
    def id_booking(self):
        return self.__id_booking

    @property
    def tanggal(self):
        return self.__tanggal

    @tanggal.setter
    def tanggal(self, value):
        self.__tanggal = value

    @property
    def status(self):
        return self.__status

    @property
    def pelanggan(self):
        return self.__pelanggan

    @property
    def fotografer(self):
        return self.__fotografer

    @property
    def paket(self):
        return self.__paket

    def buat_booking(self) -> bool:

        self.__pelanggan.booking_list.append(self)

        if hasattr(self.__fotografer, "jadwal_list"):
            self.__fotografer.jadwal_list.append(self)

        return True

    def ubah_status(self, status_baru: str) -> bool:

        if status_baru not in self.STATUS_VALID:
            raise ValueError(
                f"Status harus salah satu dari: {self.STATUS_VALID}"
            )

        self.__status = status_baru
        return True

    def batalkan_booking(self) -> bool:

        self.__status = "Dibatalkan"
        return True

    def display_info(self) -> str:

        return (
            f"ID Booking : {self.id_booking}\n"
            f"Tanggal    : {self.tanggal}\n"
            f"Status     : {self.status}\n"
            f"Pelanggan  : {self.pelanggan.nama}\n"
            f"Fotografer : {self.fotografer.nama}\n"
            f"Paket      : {self.paket.nama_paket}"
        )

    def to_dict(self) -> dict:

        return {
            "id_booking": self.id_booking,
            "tanggal": str(self.tanggal),
            "status": self.status,
            "pelanggan": self.pelanggan.nama,
            "fotografer": self.fotografer.nama,
            "paket": self.paket.nama_paket
        }
    
    def get_total_bayar(self, jumlah_paket=1) -> float:
       
        hari_inggris = self.tanggal.strftime("%A")
        terjemahan_hari = {
            "Monday": "Senin", "Tuesday": "Selasa", "Wednesday": "Rabu",
            "Thursday": "Kamis", "Friday": "Jumat", "Saturday": "Sabtu", "Sunday": "Minggu"
        }
        hari_indonesia = terjemahan_hari.get(hari_inggris, "Biasa")

      
        return self.paket.hitung_harga(jumlah_paket=jumlah_paket, hari=hari_indonesia)