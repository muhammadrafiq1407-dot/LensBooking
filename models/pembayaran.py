from datetime import datetime


class Pembayaran:

    METODE_VALID = [
        "Transfer",
        "Cash",
        "E-Wallet"
    ]

    STATUS_VALID = [
        "Belum Lunas",
        "Lunas",
        "Gagal"
    ]

    def __init__(
        self,
        booking,
        jumlah: float,
        metode_bayar: str
    ) -> None:

        if jumlah <= 0:
            raise ValueError(
                "Jumlah pembayaran harus lebih besar dari 0."
            )

        if metode_bayar not in self.METODE_VALID:
            raise ValueError(
                f"Metode pembayaran harus salah satu dari {self.METODE_VALID}"
            )

        self.__booking = booking
        self.__jumlah = jumlah
        self.__metode_bayar = metode_bayar

        self.__status_bayar = "Belum Lunas"

        self.__tanggal_bayar = None

    @property
    def booking(self):
        return self.__booking

    @property
    def jumlah(self):
        return self.__jumlah

    @property
    def metode_bayar(self):
        return self.__metode_bayar

    @property
    def status_bayar(self):
        return self.__status_bayar

    @property
    def tanggal_bayar(self):
        return self.__tanggal_bayar

    def proses_pembayaran(self) -> bool:

        if self.__status_bayar == "Lunas":
            print("Pembayaran sudah dilakukan sebelumnya.")
            return False

        self.__status_bayar = "Lunas"
        self.__tanggal_bayar = datetime.now()

        return True

    def cetak_invoice(self) -> str:

        return (
            "\n===== INVOICE =====\n"
            f"ID Booking      : {self.booking.id_booking}\n"
            f"Pelanggan       : {self.booking.pelanggan.nama}\n"
            f"Fotografer      : {self.booking.fotografer.nama}\n"
            f"Metode Bayar    : {self.metode_bayar}\n"
            f"Jumlah Bayar    : Rp {self.jumlah:,.0f}\n"
            f"Status Bayar    : {self.status_bayar}\n"
            f"Tanggal Bayar   : {self.tanggal_bayar}\n"
            "===================\n"
        )

    def display_info(self) -> str:

        return (
            f"Metode Bayar : {self.metode_bayar}\n"
            f"Jumlah       : Rp {self.jumlah:,.0f}\n"
            f"Status       : {self.status_bayar}"
        )

    def to_dict(self) -> dict:

        return {
            "id_booking": self.booking.id_booking,
            "jumlah": self.jumlah,
            "metode_bayar": self.metode_bayar,
            "status_bayar": self.status_bayar,
            "tanggal_bayar": (
                self.tanggal_bayar.isoformat()
                if self.tanggal_bayar
                else None
            )
        }