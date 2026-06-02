
class DiskonMixin:
    def apply_discount(self, total_harga, jumlah_paket=1, hari="Biasa", jenis_paket=""):
        total_diskon_persen = 0

        if total_harga > 2000000:
            total_diskon_persen += 10
            
        if jumlah_paket >= 2:
            total_diskon_persen += 5
            
        if hari.lower() == "jumat" and jenis_paket == "Wedding":
            total_diskon_persen += 15
            
        if total_diskon_persen > 25:
            total_diskon_persen = 25
            
        potongan = total_harga * (total_diskon_persen / 100)
        harga_akhir = total_harga - potongan
        
        return harga_akhir, total_diskon_persen