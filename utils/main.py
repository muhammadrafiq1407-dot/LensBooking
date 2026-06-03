import sys
import os
from datetime import datetime


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)


try:
    from models.admin import Admin
    from models.booking import Booking
    from models.fotografer import Fotografer
    from models.pelanggan import Pelanggan 
    from models.pembayaran import Pembayaran
    from models.laporan import Laporan
    from models.paket_foto import PaketWedding, PaketWisuda
except ImportError as e:
    print(f"[ERROR IMPLEMENTASI] Gagal mengimpor modul: {e}")
    print("Silakan periksa kembali penamaan file atau folder di dalam direktori 'models'.")
    sys.exit(1)


def cetak_header(judul: str):
    """Fungsi pembantu untuk mempercantik tampilan output di terminal"""
    print("\n" + "=" * 65)
    print(f"{judul.center(65)}")
    print("=" * 65)


def main():
    cetak_header("SISTEM MANAJEMEN PEMESANAN FOTOGRAFI (LENSBOOKING)")

    try:

        print("[*] Menginisialisasi akun Administrator...")
        admin = Admin(
            id="A001",
            nama="Rafiq",
            username="admin",
            password="admin123"
        )

        # Proses verifikasi login
        if not admin.login("admin123"):
            print("[-] Proses dihentikan: Akses Admin ditolak.")
            return


        cetak_header("MANAJEMEN LAYANAN PAKET FOTO OLEH ADMIN")
        
        paket_wedding = PaketWedding(
            id_paket="PW001", nama_paket="Wedding Premium", harga=5000000, durasi=8, dekorasi=True
        )
        paket_wisuda = PaketWisuda(
            id_paket="PS001", nama_paket="Wisuda Gold", harga=1500000, durasi=3, jumlah_orang=8
        )

        # Menambahkan data paket ke dalam sistem admin
        admin.tambah_paket(paket_wedding)
        admin.tambah_paket(paket_wisuda)

        print("\n[+] Daftar Paket Tersedia Saat Ini:")
        for paket in admin.lihat_laporan():
            print(f"    - [{paket.id_paket}] {paket.nama_paket:<18} | Tarif: Rp {paket.harga:,.0f}")


        cetak_header("REGISTRASI PELANGGAN & FOTOGRAFER")
        
        pelanggan = Pelanggan(
            id="P001", nama="Budi", alamat="Jakarta", telepon="081234567890"
        )
        fotografer = Fotografer(
            id="F001", nama="Andi", spesialisasi="Wedding", pengalaman=5
        )

        print(f"[+] Client Baru Berhasil Didaftarkan : {pelanggan.nama} ({pelanggan.alamat})")
        print(f"[+] Fotografer Ditugaskan           : {fotografer.nama} (Spesialisasi: {fotografer.spesialisasi})")


        cetak_header("SISTEM RESERVASI & JADWAL PEMESANAN")
        
        # Skenario pemesanan pada tanggal 6 Juni 2025 (Hari Jumat)
        booking = Booking(
            id_booking="BK001",
            tanggal=datetime(2025, 6, 6),
            pelanggan=pelanggan,
            fotografer=fotografer,
            paket=paket_wedding
        )

        if booking.buat_booking():
            print("[+] Reservasi berhasil disimpan ke sistem.")
        
        print("\n--- Ringkasan Dokumen Reservasi ---")
        print(booking.display_info())

    
        cetak_header("RINCIAN KALKULASI HARGA & DISKON KHUSUS")
        
        # Memesan sejumlah 2 paket pada hari Jumat (Memicu logika DiskonMixin)
        total_bayar = booking.get_total_bayar(jumlah_paket=2)
        
        print(f"-> Item Pemesanan  : {booking.paket.nama_paket} (x2)")
        print(f"-> Hari Pelaksanaan: {booking.tanggal.strftime('%A')} (Jumat / Promo Hari Khusus)")
        print(f"-> Total Kewajiban : Rp {total_bayar:,.0f} (Sudah Termasuk Potongan Skema Diskon)")

        
        cetak_header("EKSEKUSI LAYANAN & PROSES CHECKOUT")
        
        fotografer.update_status(booking_id="BK001", status="Selesai")
        print(f"[*] Update Status Pekerjaan: Lapangan Telah dinyatakan '{booking.status}'")


        pembayaran = Pembayaran(
            booking=booking,
            jumlah=total_bayar,
            metode_bayar="Transfer"
        )
        pembayaran.proses_pembayaran()
        
        
        print(pembayaran.cetak_invoice())

        
        cetak_header("REKAPITULASI LAPORAN EKONOMI (AUDIT)")
        
        laporan = Laporan()
        laporan.tambah_data_booking(booking)


        laporan.laporan_harian(datetime(2025, 6, 6))
        laporan.laporan_mingguan(datetime(2025, 6, 1), datetime(2025, 6, 7))
        laporan.laporan_bulanan(tahun=2025, month=6)

    
        cetak_header("AUDIT INTERNAL MASTER PROFILE DATA")
        
        print(" [1] Identitas Akun Pelanggan:")
        print(pelanggan.display_info())
        
        print("\n [2] Identitas Akun Partner Fotografer:")
        print(fotografer.display_info())
        
        print("\n [3] Identitas Akun Administrator Utama:")
        print(admin.display_info())

    except Exception as error_sistem:
        
        print(f"\n[CRITICAL RUNTIME ERROR] Program terhenti karena kegagalan internal:")
        print(f"Detail Kesalahan: {error_sistem}")
        print("\nSaran: Periksa keselarasan property/method antara model-model class Anda.")


if __name__ == "__main__":
    main()