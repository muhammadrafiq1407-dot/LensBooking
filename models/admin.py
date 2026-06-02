from .user import User


class Admin(User):
    def __init__(self, id: str, nama: str, username: str, password: str) -> None:
        super().__init__(id=id, nama=nama)
        self.__username = username
        self.__password = password
        self.paket_list: list = []

    @property
    def username(self) -> str:
        return self.__username

    @property
    def password(self) -> str:
        return "*" * len(self.__password)


    def set_password(self, new_password: str) -> None:
        if len(new_password) < 5:
            raise ValueError("Password harus memiliki minimal 5 karakter.")
        self.__password = new_password


    def login(self, password: str) -> bool:
        if password == self.__password:
            print("Login berhasil sebagai Admin.")
            return True
        print("Login gagal: Password salah.")
        return False


    def tambah_paket(self, paket) -> bool:
        if paket not in self.paket_list:
            self.paket_list.append(paket)
            print(f"Paket '{paket.nama}' berhasil ditambahkan.")
            return True
        print(f"Paket '{paket.nama}' sudah ada.")
        return False


    def hapus_paket(self, paket) -> bool:
        for p in self.paket_list:
            if p.id == paket.id:
                self.paket_list.remove(paket)
                print(f"Paket dengan ID '{paket.id}' berhasil dihapus.")
                return True
        print(f"Paket dengan ID '{paket.id}' tidak ditemukan.")
        return False

    def lihat_laporan(self) -> list:
        return self.paket_list.copy()

    def display_info(self) -> str:
        return f"Admin: {self.nama}\nUsername: {self.username}"

    def get_role(self) -> str:
        return "Admin"

    def to_dict(self) -> dict:
        base =super().to_dict()
        base.update({
            "username": self.username,
            "role": self.get_role(),
            "total_paket": len(self.paket_list)
        })
        return base
