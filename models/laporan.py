from datetime import datetime

class Laporan:
    
    def __init__(self):
        self.__data_booking = [] 

    def tambah_data_booking(self, booking):
        self.__data_booking.append(booking)

    def laporan_harian(self, tanggal_cari: datetime):
        """===> Laporan HArian <==="""
        print(f"\n=== Laporan Harian: {tanggal_cari.strftime('%d %B %Y')} ===")
        total_pendapatan = 0
        jumlah_transaksi = 0
        
        for booking in self.__data_booking:
            if booking.tanggal.date() == tanggal_cari.date() and booking.status == "Selesai":
                total_pendapatan += booking.get_total_bayar(jumlah_paket=1) 
                jumlah_transaksi += 1
                
        print(f"Total Transaksi : {jumlah_transaksi}")
        print(f"Total Pendapatan: Rp {total_pendapatan:,.2f}")
        print("===========================================")

    def laporan_mingguan(self, tanggal_awal: datetime, tanggal_akhir: datetime):
        """===< Laporan Mingguan >==="""
        print(f"\n=== Laporan Mingguan: {tanggal_awal.strftime('%d %b')} s/d {tanggal_akhir.strftime('%d %b %Y')} ===")
        total_pendapatan = 0
        jumlah_transaksi = 0
        
        for booking in self.__data_booking:
            if booking.status == "Selesai":
                if tanggal_awal.date() <= booking.tanggal.date() <= tanggal_akhir.date():
                    total_pendapatan += booking.get_total_bayar()
                    jumlah_transaksi += 1
                    
        print(f"Total Transaksi : {jumlah_transaksi}")
        print(f"Total Pendapatan: Rp {total_pendapatan:,.2f}")
        print("==============================================================")

    def laporan_bulanan(self, tahun: int, bulan: int):
        """<===> Laporan Bulanan <===>"""
        print(f"\n=== Laporan Bulanan: Bulan {bulan} Tahun {tahun} ===")
        total_pendapatan = 0
        jumlah_transaksi = 0
        
        for booking in self.__data_booking:
            if booking.status == "Selesai":
                if booking.tanggal.year == tahun and booking.tanggal.month == bulan:
                    total_pendapatan += booking.get_total_bayar()
                    jumlah_transaksi += 1
                    
        print(f"Total Transaksi : {jumlah_transaksi}")
        print(f"Total Pendapatan: Rp {total_pendapatan:,.2f}")
        print("===============================================")