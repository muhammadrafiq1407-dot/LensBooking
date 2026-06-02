from abc import ABC, abstractmethod
from mixins.Diskon_mixin import DiskonMixin

class PaketFoto(ABC):
    def __init__(self, id_paket, nama_paket, harga, durasi):
        self.__id_paket = id_paket
        self.__nama_paket = nama_paket
        self.__harga = harga
        self.__durasi = durasi

    def get_id_paket(self): return self.__id_paket
    def get_nama_paket(self): return self.__nama_paket
    def get_harga_dasar(self): return self.__harga
    def get_durasi(self): return self.__durasi

    @abstractmethod
    def hitung_harga(self, jumlah_paket=1, hari="Biasa"):
        pass


class PaketWedding(PaketFoto, DiskonMixin):
    def __init__(self, id_paket, nama_paket, harga, durasi, dekorasi):
        PaketFoto.__init__(self, id_paket, nama_paket, harga, durasi)
        self.__dekorasi = dekorasi 

    def hitung_harga(self, jumlah_paket=1, hari="Biasa"):
        harga_dasar = self.get_harga_dasar()
        biaya_dekorasi = 1500000 if self.__dekorasi else 0
        
        total_sementara = (harga_dasar + biaya_dekorasi) * jumlah_paket
        
        harga_final, persen_diskon = self.apply_discount(
            total_sementara, jumlah_paket, hari, jenis_paket="Wedding"
        )
        return harga_final


class PaketWisuda(PaketFoto, DiskonMixin):
    def __init__(self, id_paket, nama_paket, harga, durasi, jumlah_orang):
        PaketFoto.__init__(self, id_paket, nama_paket, harga, durasi)
        self.__jumlah_orang = jumlah_orang

    def hitung_harga(self, jumlah_paket=1, hari="Biasa"):
        harga_dasar = self.get_harga_dasar()
        biaya_ekstra = (self.__jumlah_orang - 5) * 50000 if self.__jumlah_orang > 5 else 0
        
        total_sementara = (harga_dasar + biaya_ekstra) * jumlah_paket
        
        harga_final, persen_diskon = self.apply_discount(
            total_sementara, jumlah_paket, hari, jenis_paket="Wisuda"
        )
        return harga_final