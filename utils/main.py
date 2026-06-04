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
    print(f"[ERROR IMPORT] Gagal memuat modul: {e}")
    sys.exit(1)


database = {
    "admin": Admin(id="A001", nama="Rafiq", username="admin", password="admin123"),
    "paket": [],
    "pelanggan": [],
    "fotografer": [],
    "booking": [],
    "laporan": Laporan()
}

def seed_data():
    """Mengisi data awal agar aplikasi tidak kosong saat pertama kali dijalankan"""
    
    database["paket"].append(PaketWedding("PW001", "Wedding Premium", 5000000, 8, True))
    database["paket"].append(PaketWisuda("PS001", "Wisuda Gold", 1500000, 3, 8))
    
    
    for p in database["paket"]:
        database["admin"].tambah_paket(p)

    
    database["pelanggan"].append(Pelanggan("P001", "Budi", "Jakarta", "081234567890"))
    database["pelanggan"].append(Pelanggan("P002", "Siti", "Bandung", "089876543210"))
    
    # Seed Fotografer
    database["fotografer"].append(Fotografer("F001", "Andi", "Wedding", 5))
    database["fotografer"].append(Fotografer("F002", "Chandra", "Wisuda", 3))


def menu_crud_paket():
    while True:
        print("\n=== KELOLA DATA PAKET FOTO (CRUD) ===")
        print("1. Tambah Paket Baru (Create)")
        print("2. Lihat Semua Paket (Read)")
        print("3. Hapus Paket Foto  (Delete)")
        print("0. Kembali ke Menu Utama")
        pilihan = input("Pilih menu [0-3]: ").strip()

        if pilihan == "1":
            print("\n--- Tambah Paket Baru ---")
            jenis = input("Jenis Paket (1: Wedding, 2: Wisuda): ").strip()
            id_paket = input("ID Paket: ").strip()
            nama = input("Nama Paket: ").strip()
            try:
                harga = float(input("Harga Paket (Rp): "))
                durasi = int(input("Durasi Kerja (Jam): "))
                
                if jenis == "1":
                    dekor = input("Termasuk Dekorasi? (y/n): ").strip().lower() == "y"
                    baru = PaketWedding(id_paket, nama, harga, durasi, dekor)
                elif jenis == "2":
                    orang = int(input("Maksimal Jumlah Orang: "))
                    baru = PaketWisuda(id_paket, nama, harga, durasi, orang)
                else:
                    print("[-] Jenis paket tidak valid!")
                    continue
                
                if database["admin"].tambah_paket(baru):
                    database["paket"].append(baru)
            except ValueError:
                print("[-] Input angka tidak valid!")

        elif pilihan == "2":
            print("\n--- Daftar Semua Paket Foto ---")
            paket_list = database["admin"].lihat_laporan()
            if not paket_list:
                print("Belum ada data paket.")
            for p in paket_list:
                print(f"- [{p.id_paket}] {p.nama_paket} | Harga: Rp {p.harga:,.0f} | Durasi: {p.durasi} Jam")

        elif pilihan == "3":
            print("\n--- Hapus Paket Foto ---")
            id_hapus = input("Masukkan ID Paket yang akan dihapus: ").strip()
            target = None
            for p in database["paket"]:
                if p.id_paket == id_hapus:
                    target = p
                    break
            if target:
                if database["admin"].hapus_paket(target):
                    database["paket"].remove(target)
            else:
                print("[-] Paket tidak ditemukan.")

        elif pilihan == "0":
            break
        else:
            print("[-] Pilihan tidak tersedia.")


def menu_crud_pelanggan():
    while True:
        print("\n=== KELOLA DATA PELANGGAN  ===")
        print("1. Registrasi Pelanggan Baru ")
        print("2. Tampilkan Semua Pelanggan " \
        ")")
        print("0. Kembali ke Menu Utama")
        pilihan = input("Pilih menu [0-2]: ").strip()

        if pilihan == "1":
            print("\n--- Registrasi Pelanggan ---")
            id_p = input("ID Pelanggan: ").strip()
            nama = input("Nama Lengkap: ").strip()
            alamat = input("Alamat: ").strip()
            telp = input("No Telepon: ").strip()
            
            baru = Pelanggan(id_p, nama, alamat, telp)
            database["pelanggan"].append(baru)
            print(f"[+] Pelanggan '{nama}' berhasil didaftarkan.")

        elif pilihan == "2":
            print("\n--- Daftar Pelanggan terdaftar ---")
            if not database["pelanggan"]:
                print("Belum ada pelanggan terdaftar.")
            for p in database["pelanggan"]:
                print(f"- ID: {p.id} | Nama: {p.nama} | Alamat: {p.alamat} | Telp: {p.telepon}")

        elif pilihan == "0":
            break
        else:
            print("[-] Pilihan tidak tersedia.")


def menu_crud_booking():
    while True:
        print("\n=== KELOLA RESERVASI & TRANSAKSI  ===")
        print("1. Buat Reservasi Booking Baru ")
        print("2. Lihat Semua Riwayat Booking ")
        print("3. Update Status Pekerjaan Lapangan ")
        print("4. Proses Pembayaran & Invoice ")
        print("5. Batalkan Jadwal Booking ")
        print("0. Kembali ke Menu Utama")
        pilihan = input("Pilih menu [0-5]: ").strip()

        if pilihan == "1":
            print("\n--- Buat Booking Baru ---")
            id_b = input("ID Booking Baru: ").strip()
            tgl_str = input("Tanggal Acara (Format YYYY-MM-DD): ").strip()
            try:
                tanggal_obj = datetime.strptime(tgl_str, "%Y-%m-%d")
            except ValueError:
                print("[-] Format tanggal salah!")
                continue

            
            print("\nPilih Pelanggan:")
            for idx, p in enumerate(database["pelanggan"]):
                print(f"{idx+1}. [{p.id}] {p.nama}")
            p_pilih = int(input("Nomor Pelanggan: ")) - 1
            
            
            print("\nPilih Fotografer:")
            for idx, f in enumerate(database["fotografer"]):
                print(f"{idx+1}. [{f.id}] {f.nama} ({f.spesialisasi})")
            f_pilih = int(input("Nomor Fotografer: ")) - 1
            
            
            print("\nPilih Paket Foto:")
            for idx, pkt in enumerate(database["paket"]):
                print(f"{idx+1}. [{pkt.id_paket}] {pkt.nama_paket}")
            pkt_pilih = int(input("Nomor Paket: ")) - 1

            try:
                obj_p = database["pelanggan"][p_pilih]
                obj_f = database["fotografer"][f_pilih]
                obj_pkt = database["paket"][pkt_pilih]
                
                baru_booking = Booking(id_b, tanggal_obj, obj_p, obj_f, obj_pkt)
                if baru_booking.buat_booking():
                    database["booking"].append(baru_booking)
                    database["laporan"].tambah_data_booking(baru_booking)
                    print("[+] Booking berhasil dibuat dan dijadwalkan!")
            except IndexError:
                print("[-] Nomor pilihan entitas tidak ditemukan.")

        elif pilihan == "2":
            print("\n--- Daftar Info Seluruh Booking ---")
            if not database["booking"]:
                print("Belum ada data booking.")
            for b in database["booking"]:
                print("-" * 40)
                print(b.display_info())

        elif pilihan == "3":
            print("\n--- Update Status Kerja Lapangan (Fotografer) ---")
            id_b = input("Masukkan ID Booking: ").strip()
            status_baru = input("Status Baru (Diproses/Selesai): ").strip()
            
            
            updated = False
            for f in database["fotografer"]:
                if f.update_status(id_b, status_baru):
                    updated = True
                    break
            if updated:
                print("[+] Status booking berhasil diperbarui oleh Fotografer.")
            else:
                print("[-] ID Booking tidak ditemukan pada jadwal fotografer manapun.")

        elif pilihan == "4":
            print("\n--- Proses Kasir Pembayaran & Cetak Nota ---")
            id_b = input("Masukkan ID Booking untuk Pembayaran: ").strip()
            target_b = None
            for b in database["booking"]:
                if b.id_booking == id_b:
                    target_b = b
                    break
            
            if target_b:
                qty = int(input("Jumlah kuantitas paket yang disewa: "))
                total_tagihan = target_b.get_total_bayar(jumlah_paket=qty)
                print(f"Total biaya setelah kalkulasi diskon harian: Rp {total_tagihan:,.0f}")
                
                metode = input("Metode Bayar (Transfer/Cash/E-Wallet): ").strip()
                try:
                    pembayaran = Pembayaran(target_b, total_tagihan, metode)
                    if pembayaran.proses_pembayaran():
                        print(pembayaran.cetak_invoice())
                except ValueError as e:
                    print(f"[-] Gagal memproses: {e}")
            else:
                print("[-] ID Booking tidak dikenali.")

        elif pilihan == "5":
            print("\n--- Pembatalan Agenda Booking ---")
            id_b = input("Masukkan ID Booking yang akan dicancel: ").strip()
            found = False
            for b in database["booking"]:
                if b.id_booking == id_b:
                    b.batalkan_booking()
                    print(f"[+] Booking ID {id_b} telah diubah status menjadi Dibatalkan.")
                    found = True
                    break
            if not found:
                print("[-] ID Booking tidak valid.")

        elif pilihan == "0":
            break
        else:
            print("[-] Pilihan salah.")


def menu_laporan():
    while True:
        print("\n=== MODUL AUDIT LAPORAN PENDAPATAN ===")
        print("1. Laporan Harian")
        print("2. Laporan Bulanan")
        print("0. Kembali ke Menu Utama")
        pilihan = input("Pilih menu [0-2]: ").strip()

        if pilihan == "1":
            tgl_s = input("Masukkan Tanggal Audit (YYYY-MM-DD): ").strip()
            try:
                tgl = datetime.strptime(tgl_s, "%Y-%m-%d")
                database["laporan"].laporan_harian(tgl)
            except ValueError:
                print("[-] Format tanggal salah.")
        elif pilihan == "2":
            try:
                tahun = int(input("Tahun (YYYY): "))
                bulan = int(input("Bulan (1-12): "))
                database["laporan"].laporan_bulanan(tahun, bulan)
            except ValueError:
                print("[-] Input tahun/bulan wajib angka.")
        elif pilihan == "0":
            break


def main():
    seed_data()  
    # Validasi Login Admin Utama
    print("=" * 60)
    print("      SELAMAT DATANG DI CONSOLE APP LENSBOOKING SYSTEM       ")
    print("=" * 60)
    print("[*] Otentikasi Akses Dibutuhkan.")
    username = input("Username Admin: ").strip()
    password = input("Password Admin: ").strip()
    
    if username == "admin" and database["admin"].login(password):

        while True:
            print("\n" + "="*45)
            print("               MENU UTAMA APLIKASI            ")
            print("="*45)
            print("1. Kelola Layanan Paket Foto ")
            print("2. Kelola Registrasi Pelanggan ")
            print("3. Kelola Transaksi Pemesanan ")
            print("4. Lihat Laporan Keuangan ")
            print("0. Keluar dari Aplikasi")
            print("="*45)
            
            pilihan = input("Masukkan pilihan menu [0-4]: ").strip()
            
            if pilihan == "1":
                menu_crud_paket()
            elif pilihan == "2":
                menu_crud_pelanggan()
            elif pilihan == "3":
                menu_crud_booking()
            elif pilihan == "4":
                menu_laporan()
            elif pilihan == "0":
                print("\n[+] Terima kasih telah menggunakan layanan LensBooking. Aplikasi ditutup.")
                break
            else:
                print("[-] Menu tidak valid! Masukkan angka yang tertera di daftar.")
    else:
        print("[-] Login Gagal: Kombinasi akun administrator tidak cocok!")

if __name__ == "__main__":
    main()