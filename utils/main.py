import sys
import os

# Mengambil path root project (LENSBOOKING)
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

# Sekarang kita bisa import dengan absolut path dari root
from datetime import datetime
from models.admin import Admin
from models.booking import Booking
from models.fotografer import Fotografer
# Pastikan kamu membuat file pelanggan.py karena di main.py di-import!
from models.pelanggan import Pelanggan 
from models.pembayaran import Pembayaran
from models.laporan import Laporan
from models.paket_foto import PaketWedding, PaketWisuda

def main():
    print("=" * 50)
    print(" SISTEM PEMESANAN JASA FOTOGRAFI ")
    print("=" * 50)

    # ==========================
    # ADMIN
    # ==========================
    admin = Admin(
        id="A001",
        nama="Rafiq",
        username="admin",
        password="admin123"
    )

    admin.login("admin123")

    # ==========================
    # PAKET FOTO
    # ==========================
    paket_wedding = PaketWedding(
        id_paket="PW001",
        nama_paket="Wedding Premium",
        harga=5000000,
        durasi=8,
        dekorasi=True
    )

    paket_wisuda = PaketWisuda(
        id_paket="PS001",
        nama_paket="Wisuda Gold",
        harga=1500000,
        durasi=3,
        jumlah_orang=8
    )

    admin.tambah_paket(paket_wedding)
    admin.tambah_paket(paket_wisuda)

    print("\n=== Data Paket ===")
    for paket in admin.lihat_laporan():
        print("-", paket.get_nama_paket())

    # ==========================
    # PELANGGAN
    # ==========================
    pelanggan = Pelanggan(
        id="P001",
        nama="Budi",
        alamat="Jakarta",
        telepon="081234567890"
    )

    # ==========================
    # FOTOGRAFER
    # ==========================
    fotografer = Fotografer(
        id="F001",
        nama="Andi",
        spesialisasi="Wedding",
        pengalaman=5
    )

    # ==========================
    # BOOKING
    # ==========================
    booking = Booking(
        id_booking="BK001",
        tanggal=datetime(2025, 6, 6),  # Jumat
        pelanggan=pelanggan,
        fotografer=fotografer,
        paket=paket_wedding
    )

    booking.buat_booking()

    print("\n=== DETAIL BOOKING ===")
    print(booking.display_info())

    # ==========================
    # HITUNG TOTAL BAYAR
    # ==========================
    total_bayar = booking.get_total_bayar(
        jumlah_paket=2
    )

    print("\n=== TOTAL PEMBAYARAN ===")
    print(f"Total Bayar : Rp {total_bayar:,.0f}")

    # ==========================
    # UPDATE STATUS
    # ==========================
    fotografer.update_status(
        booking_id="BK001",
        status="Selesai"
    )

    print("\nStatus Booking :", booking.status)

    # ==========================
    # PEMBAYARAN
    # ==========================
    pembayaran = Pembayaran(
        booking=booking,
        jumlah=total_bayar,
        metode_bayar="Transfer"
    )

    pembayaran.proses_pembayaran()

    print(pembayaran.cetak_invoice())

    # ==========================
    # LAPORAN
    # ==========================
    laporan = Laporan()

    laporan.tambah_data_booking(booking)

    print("\n")
    laporan.laporan_harian(
        datetime(2025, 6, 6)
    )

    laporan.laporan_mingguan(
        datetime(2025, 6, 1),
        datetime(2025, 6, 7)
    )

    laporan.laporan_bulanan(
        tahun=2025,
        bulan=6
    )

    # ==========================
    # DATA USER
    # ==========================
    print("\n=== DATA PELANGGAN ===")
    print(pelanggan.display_info())

    print("\n=== DATA FOTOGRAFER ===")
    print(fotografer.display_info())

    print("\n=== DATA ADMIN ===")
    print(admin.display_info())


if __name__ == "__main__":
    main()