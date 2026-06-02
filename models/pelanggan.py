from .user import User

class Pelanggan(User):
    def __init__(self, id: str, nama: str, alamat: str, telepon:str) -> None:
        super().__init__(id=id, nama=nama)
        self.alamat = alamat
        self.telepon = telepon
        self.booking_list: list = []

    @property
    def alamat(self) -> str:
        return self.__alamat
    @alamat.setter
    def alamat(self, value: str) -> None:
        if not value or not value.strip():
            raise ValueError("Alamat tidak boleh kosong.")
        self.__alamat = value.strip()

    @property
    def telepon(self) -> str:
        return self.__telepon
    
    @telepon.setter
    def telepon(self, value: str) -> None:
        if not value or not value.strip():
            raise ValueError("Telepon tidak boleh kosong.")
        value_clean = value.strip().replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
        if not value_clean.replace("+", "").isdigit():
            raise ValueError("Telepon harus berupa angka.")
        digit_count = len(value_clean.replace("+", ""))
        if digit_count < 12:
            raise ValueError("Telepon harus memiliki minimal 12 digit.")
        self.__telepon = value_clean

    def booking_jadwal(self, jadwal) -> bool:
        if jadwal not in self.booking_list:
            self.booking_list.append(jadwal)
            return True
        print(f"Jadwal '{jadwal.nama}' sudah di booking.")
        return False
    
    def lihat_booking(self) -> list:
        return self.booking_list.copy()
    
    def get_total_booking(self) -> int:
        return len(self.booking_list)
    
    def display_info(self) -> str:
        return (
            f"Pelanggan: {self.nama}\n"
            f"Alamat: {self.alamat}\n"
            f"Telepon: {self.telepon}\n"
            f"Total Booking: {len(self.booking_list)}"
        )
    
    def get_role(self) -> str:
        return "Pelanggan"
    
    def to_dict(self) -> dict:
        base = super().to_dict()
        base.update( {
            "alamat": self.alamat,
            "telepon": self.telepon,
            "total_booking": len(self.booking_list)
        })
        return base
