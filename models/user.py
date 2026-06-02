from abc import ABC, abstractmethod
from datetime import datetime


class User(ABC):
    def __init__(self, id: str, nama: str) -> None:
        self.__id = id
        self.nama = nama
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
            "created_at": self.created_at.isoformat() if self.created_at else None
        }