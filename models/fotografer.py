from .user import User


class Fotografer(User):

    def __init__(
        self,
        id: str,
        nama: str,
        spesialisasi: str,
        pengalaman: int
    ) -> None:

        super().__init__(id=id, nama=nama)

        self.spesialisasi = spesialisasi
        self.pengalaman = pengalaman

        self.jadwal_list: list = []

    @property
    def spesialisasi(self) -> str:
        return self.__spesialisasi

    @spesialisasi.setter
    def spesialisasi(self, value: str) -> None:
        if not value or not value.strip():
            raise ValueError("Spesialisasi tidak boleh kosong.")
        self.__spesialisasi = value.strip()

    @property
    def pengalaman(self) -> int:
        return self.__pengalaman

    @pengalaman.setter
    def pengalaman(self, value: int) -> None:
        if value < 0:
            raise ValueError("Pengalaman tidak boleh negatif.")
        self.__pengalaman = value

    def lihat_jadwal(self) -> list:
        return self.jadwal_list.copy()

    def update_status(self, booking_id: str, status: str) -> bool:

        for booking in self.jadwal_list:
            if booking.id_booking == booking_id:
                booking.ubah_status(status)
                return True

        return False

    def tambah_jadwal(self, booking) -> bool:

        if booking not in self.jadwal_list:
            self.jadwal_list.append(booking)
            return True

        return False

    def display_info(self) -> str:
        return (
            f"Fotografer: {self.nama}\n"
            f"Spesialisasi: {self.spesialisasi}\n"
            f"Pengalaman: {self.pengalaman} tahun\n"
            f"Total Booking: {len(self.jadwal_list)}"
        )

    def get_role(self) -> str:
        return "Fotografer"

    def to_dict(self) -> dict:

        base = super().to_dict()

        base.update({
            "spesialisasi": self.spesialisasi,
            "pengalaman": self.pengalaman,
            "total_booking": len(self.jadwal_list)
        })

        return base