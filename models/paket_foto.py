from abc import ABC, abstractmethod

from mixins.Diskon_mixin import DiskonMixin

class PaketFoto(ABC):
    """Abstract Base Class untuk semua paket foto."""
    
    def __init__(self, id_paket, nama_paket, harga, durasi, deskripsi=""):
        self.__id_paket = id_paket
        self.__nama_paket = nama_paket
        self.__harga = harga
        self.__durasi = durasi
        self.__deskripsi = deskripsi

    def get_id_paket(self): return self.__id_paket
    def get_nama_paket(self): return self.__nama_paket
    def get_harga_dasar(self): return self.__harga
    def get_durasi(self): return self.__durasi
    def get_deskripsi(self): return self.__deskripsi

    @abstractmethod
    def hitung_harga(self, jumlah_paket=1, hari="Biasa"):
        pass

class PaketWedding(PaketFoto, DiskonMixin):
    def __init__(self, id_paket, nama_paket, harga, durasi, dekorasi, deskripsi=""):
        PaketFoto.__init__(self, id_paket, nama_paket, harga, durasi, deskripsi)
        self.__dekorasi = dekorasi 

    def hitung_harga(self, jumlah_paket=1, hari="Biasa"):
        harga_dasar = self.get_harga_dasar()
        biaya_dekorasi = 1500000 if self.__dekorasi else 0
        total_sementara = (harga_dasar + biaya_dekorasi) * jumlah_paket
        
        hasil_diskon = self.apply_discount(total_sementara)
        return hasil_diskon[0] if isinstance(hasil_diskon, tuple) else hasil_diskon

class PaketWisuda(PaketFoto, DiskonMixin):
    def __init__(self, id_paket, nama_paket, harga, durasi, jumlah_orang, deskripsi=""):
        PaketFoto.__init__(self, id_paket, nama_paket, harga, durasi, deskripsi)
        self.__jumlah_orang = jumlah_orang

    def hitung_harga(self, jumlah_paket=1, hari="Biasa"):
        harga_dasar = self.get_harga_dasar()
        biaya_ekstra = (self.__jumlah_orang - 5) * 50000 if self.__jumlah_orang > 5 else 0
        total_sementara = (harga_dasar + biaya_ekstra) * jumlah_paket
        
        hasil_diskon = self.apply_discount(total_sementara)
        return hasil_diskon[0] if isinstance(hasil_diskon, tuple) else hasil_diskon

class PaketCustom(PaketFoto, DiskonMixin):
    """Paket fleksibel untuk acara seperti Ulang Tahun, Reuni, dll."""
    def __init__(self, id_paket, nama_paket, harga_per_jam, durasi, deskripsi=""):
        harga_total = harga_per_jam * durasi
        PaketFoto.__init__(self, id_paket, nama_paket, harga_total, durasi, deskripsi)
        self.__harga_per_jam = harga_per_jam

    def hitung_harga(self, jumlah_paket=1, hari="Biasa"):
        harga_dasar = self.get_harga_dasar()
        total_sementara = harga_dasar * jumlah_paket
        
        hasil_diskon = self.apply_discount(total_sementara)
        return hasil_diskon[0] if isinstance(hasil_diskon, tuple) else hasil_diskon