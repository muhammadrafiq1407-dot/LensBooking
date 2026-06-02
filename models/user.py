from abc import ABC, abstractmethod
from datetime import datetime


class User(ABC):
    def __init__(self, id: str, nama: str, noHp: str) -> None:
        self.__id = id
        self.nama = nama
        self.noHp = noHp
        self.__created_at: datetime = datetime.now()

    @property
    def id(self) -> str:
        return self.__id

    @property
    def nama(self):
        return self.__nama

    @nama.setter
    def nama(self, value: str) -> None:
        if not value or not value.strip():
            raise ValueError("Nama tidak boleh kosong.")
        self.__nama = value.strip()

    @property
    def noHp(self):
        return self.__noHp

    @noHp.setter
    def noHp(self, value: str) -> None:
        if not value or not value.strip():
            raise ValueError("Nomor HP tidak boleh kosong.")
        value_clean = value.strip().replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
        if not value_clean.replace("+", "").isdigit():
            raise ValueError("Nomor HP harus berupa angka.")
        digit_count = len(value_clean.replace("+", ""))
        if digit_count < 12:
            raise ValueError("Nomor HP harus memiliki minimal 12 digit.")
        self.__noHp = value_clean

    @property
    def created_at(self) -> datetime:
        return self.__created_at

    @abstractmethod
    def display_info(self) -> str:
        pass

    @abstractmethod
    def get_role(self) -> str:
        pass

    def __str__(self) -> str:
        return f"{self.get_role()}: {self.nama}, No HP: {self.noHp})"
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nama": self.nama,
            "noHp": self.noHp,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }