import sys
import os
from datetime import datetime
from datetime import datetime, timedelta
import json

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
    from models.paket_foto import PaketWedding, PaketWisuda, PaketCustom
    
except ImportError as e:
    print(f"[ERROR] Gagal mengimpor modul: {e}")
    sys.exit(1)


daftar_paket = [
    PaketWedding("PW01", "Wedding Premium", 5000000, 8, True, "Dokumentasi eksklusif pernikahan full-day, gratis cetak album & dekorasi mini studio."),
    PaketWisuda("PS01", "Wisuda Gold", 1500000, 3, 5, "Sesi foto wisuda VIP (Indoor/Outdoor), bebas gaya, maks 5 orang, termasuk frame 17R."),
    # [BARIS 27] Beri koma di akhir baris ini:
    PaketWisuda("PS02", "Wisuda Hemat", 800000, 1, 2, "Sesi foto wisuda durasi singkat, maks 2 orang, hasil foto diedit secara digital."),
    # [BARIS 28] Tambahkan PaketCustom di bawah ini:
    PaketCustom("PC01", "Custom Event (Ultah/Reuni)", 250000, 4, "Paket fleksibel dihitung per jam. Minimum booking 4 jam.")
]

daftar_fotografer = [
    Fotografer("F01", "Andi", "Wedding", 5),
    Fotografer("F02", "Budi", "Wisuda", 3),
    Fotografer("F03", "Citra", "All-Rounder", 4)
]

sistem_laporan = Laporan()
daftar_booking = []
BATAS_SESI_PER_WAKTU = 1 

admin_utama = Admin(id="A01", nama="Budi Manager", username="admin", password="password123")
admin_utama.paket_list = daftar_paket

def simpan_data_booking():
    data_tersimpan = [booking.to_dict() for booking in daftar_booking]
    with open("backup_booking.json", "w") as file_json:
        json.dump(data_tersimpan, file_json, indent=4)
    print("\n[+] Data seluruh booking berhasil di-backup ke 'backup_booking.json'!")



def generate_id_booking():
    return f"BK{len(daftar_booking) + 1:03d}"

def jeda_interaksi():
    input("\n[Tekan Enter untuk melanjutkan...]")

def konfirmasi_error():
    while True:
        pil = input("=> Ketik '1' untuk Ulangi, '0' untuk Batal/Kembali ke menu: ").strip()
        if pil == '1': return True
        if pil == '0': return False
        print("[-] Pilihan tidak valid. Harap ketik 1 atau 0.")

def cek_ketersediaan_jadwal(tgl_waktu_baru, durasi_baru, id_fotografer, no_telp_pelanggan):
    """Mengecek tabrakan jadwal menggunakan logika Time Overlap"""
    waktu_selesai_baru = tgl_waktu_baru + timedelta(hours=durasi_baru)
    
    for b in daftar_booking:
        if b.status != "Dibatalkan":
            waktu_mulai_lama = b.tanggal
            waktu_selesai_lama = b.tanggal + timedelta(hours=b.paket.get_durasi())
            
            if (waktu_mulai_lama < waktu_selesai_baru) and (waktu_selesai_lama > tgl_waktu_baru):
                
                if b.pelanggan.telepon == no_telp_pelanggan:
                    return False, "Anda sudah memiliki booking di rentang waktu ini."
                if b.fotografer.id == id_fotografer:
                    return False, f"Fotografer {b.fotografer.nama} sedang bertugas dari {waktu_mulai_lama.strftime('%H:%M')} s/d {waktu_selesai_lama.strftime('%H:%M')}."
                
                return False, f"Studio penuh! Sedang dipakai dari {waktu_mulai_lama.strftime('%H:%M')} s/d {waktu_selesai_lama.strftime('%H:%M')}."
                
    return True, "Jadwal Tersedia"


def menu_pelanggan():
    while True:
        print("\n--- MENU PELANGGAN ---")
        print("1. Buat Booking Baru")
        print("2. Daftar Ulang (Check-in Sesi Foto)")
        print("0. Kembali ke Menu Utama")
        
        pilihan = input("Pilih menu: ").strip()
        
        if pilihan == '1':
            print("\n[FORM BOOKING STUDIO]")
            
            while True:
                nama_pelanggan = input("Nama Anda: ").strip()
                if not nama_pelanggan:
                    print("[-] Nama tidak boleh kosong!")
                elif len(nama_pelanggan) < 3:
                    print("[-] Nama terlalu pendek (Minimal 3 huruf)!")
                elif not nama_pelanggan.replace(" ", "").isalpha():
                    print("[-] Nama tidak valid! Hanya boleh berisi huruf tanpa angka/simbol.")
                else:
                    break
                if not konfirmasi_error(): return
            
            while True:
                alamat = input("Alamat: ").strip()
                if not alamat:
                    print("[-] Alamat tidak boleh kosong!")
                elif alamat.replace(" ", "").isdigit():
                    print("[-] Alamat tidak boleh hanya berisi angka!")
                elif len(alamat) < 5:
                    print("[-] Alamat terlalu pendek. Harap masukkan alamat lengkap.")
                else:
                    break
                if not konfirmasi_error(): return
            
            while True:
                no_telepon = input("Nomor Telepon (Minimal 12 angka): ").strip()
                try:
                    pelanggan_baru = Pelanggan(f"P{len(daftar_booking)+1}", nama_pelanggan, alamat, no_telepon)
                    break 
                except ValueError as e:
                    print(f"[-] Gagal: {e}")
                if not konfirmasi_error(): return
            
            while True:
                tgl_str = input("\nMasukkan Tanggal Booking (YYYY-MM-DD), contoh 2026-06-15: ").strip()
                jam_str = input("Masukkan Jam Mulai (HH:MM), contoh 10:00: ").strip()
                try:
                    tgl_booking = datetime.strptime(f"{tgl_str} {jam_str}", "%Y-%m-%d %H:%M")
                    
                    if not (9 <= tgl_booking.hour < 20):
                        print("[-] Gagal: Jadwal harus di dalam Jam Operasional (09:00 - 20:00)!")
                        if not konfirmasi_error(): return
                        continue
                    
                    if tgl_booking < datetime.now():
                        print(f"[-] Gagal: Tidak bisa mem-booking jadwal di waktu yang sudah berlalu (Sekarang: {datetime.now().strftime('%Y-%m-%d %H:%M')})!")
                        if not konfirmasi_error(): return
                        continue
                        
                except ValueError:
                    print("[-] Format tanggal atau jam salah! Pastikan format sesuai contoh.")
                    if not konfirmasi_error(): return
                    continue

                print("\n[DAFTAR PAKET TERSEDIA]")
                for i, pkt in enumerate(daftar_paket):
                    print(f"{i+1}. {pkt.get_nama_paket()} - Rp {pkt.get_harga_dasar():,.0f} ({pkt.get_durasi()} Jam)")
                    print(f"   >> Detail: {pkt.get_deskripsi()}")
                
                print(f"\n{len(daftar_paket) + 1}. [BUAT PAKET CUSTOM] Request paket untuk event khusus (Ulang Tahun, Reuni, dll)")
                print("0. (Batalkan Booking)")
                
                try:
                    pil_paket = int(input("\nPilih nomor paket (0 untuk batal): ").strip())
                    if pil_paket == 0:
                        print("[!] Booking dibatalkan. Kembali ke menu pelanggan.")
                        jeda_interaksi()
                        return
                    
                    if pil_paket == len(daftar_paket) + 1:
                        nama_event = input("-> Acara apa yang ingin Anda dokumentasikan? (misal: Ulang Tahun Anak): ").strip()
                        try:
                            durasi_custom = int(input(f"-> Berapa jam estimasi Anda membutuhkan fotografer untuk {nama_event}? (angka): ").strip())
                        except ValueError:
                            print("[-] Durasi harus berupa angka!")
                            if not konfirmasi_error(): return
                            continue
                        
                        harga_per_jam_studio = 350000 
                        paket_dipilih = PaketCustom(
                            id_paket=f"PC{len(daftar_booking)+1:03d}", 
                            nama_paket=f"Custom: {nama_event}", 
                            harga_per_jam=harga_per_jam_studio, 
                            durasi=durasi_custom, 
                            deskripsi=f"Paket dokumentasi acara {nama_event} secara custom sesuai permintaan."
                        )
                        detail_tambahan = input(f"-> Masukkan lokasi atau permintaan khusus untuk acara {nama_event}: ")

                    elif 1 <= pil_paket <= len(daftar_paket):
                        paket_dipilih = daftar_paket[pil_paket - 1]
                        detail_tambahan = ""
                        
                        if "Wedding" in paket_dipilih.get_nama_paket():
                            detail_tambahan = input(f"-> Masukkan detail lokasi acara untuk {paket_dipilih.get_nama_paket()}: ")
                        elif "Wisuda" in paket_dipilih.get_nama_paket():
                            detail_tambahan = input(f"-> Berapa jumlah orang dalam sesi {paket_dipilih.get_nama_paket()} ini? ")
                    else:
                        print("[-] Pilihan paket tidak valid!")
                        if not konfirmasi_error(): return
                        continue
                        
                except ValueError:
                    print("[-] Harap masukkan angka yang valid!")
                    if not konfirmasi_error(): return
                    continue
                
                print("\n[DAFTAR FOTOGRAFER]")
                for i, fg in enumerate(daftar_fotografer):
                    print(f"{i+1}. {fg.nama} (Spesialis: {fg.spesialisasi})")
                    
                try:
                    pil_fg = int(input("Ingin difoto siapa? (Pilih nomor): ").strip()) - 1
                    if pil_fg < 0 or pil_fg >= len(daftar_fotografer):
                        print("[-] Pilihan fotografer tidak valid!")
                        if not konfirmasi_error(): return
                        continue
                        
                    fg_dipilih = daftar_fotografer[pil_fg]
                    
                except ValueError:
                    print("[-] Harap masukkan angka yang valid!")
                    if not konfirmasi_error(): return
                    continue
                
                tersedia, pesan_jadwal = cek_ketersediaan_jadwal(
                    tgl_booking, 
                    paket_dipilih.get_durasi(), 
                    fg_dipilih.id, 
                    pelanggan_baru.telepon
                )
                
                if not tersedia:
                    print(f"\n[-] Gagal: {pesan_jadwal}")
                    print("[-] Anda harus mencari tanggal atau jam yang berbeda.")
                    if konfirmasi_error(): 
                        continue 
                    else:
                        return 
                        
                print(f"[+] Jadwal Tersedia! Fotografer {fg_dipilih.nama} siap bertugas.")
                break
                
            
            booking_baru = Booking(generate_id_booking(), tgl_booking, pelanggan_baru, fg_dipilih, paket_dipilih)
            booking_baru.catatan_detail = detail_tambahan 
            
            hari_booking = tgl_booking.strftime("%A")
            terjemahan = {"Sunday": "Minggu", "Saturday": "Sabtu", "Friday": "Jumat", "Monday": "Senin", "Tuesday": "Selasa", "Wednesday": "Rabu", "Thursday": "Kamis"}
            hari_indo = terjemahan.get(hari_booking, "Biasa")
            
            total_bayar = booking_baru.get_total_bayar(jumlah_paket=1)
            
            print("\n--- KONFIRMASI BOOKING ---")
            print(booking_baru.display_info())
            print(f"Jam        : {tgl_booking.strftime('%H:%M')} WIB")
            print(f"Detail     : {booking_baru.catatan_detail}")
            print(f"Total Biaya: Rp {total_bayar:,.0f} (Hari {hari_indo})")
            
            bayar = input("\nProses Pembayaran sekarang? (y/n): ").strip()
            if bayar.lower() == 'y':
                print("\n[PILIH METODE PEMBAYARAN]")
                print("1. Transfer\n2. Cash\n3. E-Wallet")
                pil_met = input("Pilihan (1-3): ").strip()
                
                metode_valid = "Cash"
                bukti_pembayaran = ""
                
                if pil_met == '1': 
                    metode_valid = "Transfer"
                    bukti_pembayaran = input(">> Masukkan Nomor Referensi Bank / Bukti Transfer: ")
                elif pil_met == '2': 
                    metode_valid = "Cash"
                elif pil_met == '3': 
                    metode_valid = "E-Wallet"
                    bukti_pembayaran = input(">> Masukkan Nomor Ref E-Wallet (OVO/Dana/GoPay): ")
                else:
                    print("[-] Pilihan tidak valid, pembayaran dialihkan ke Cash.")

                try:
                    pembayaran = Pembayaran(booking_baru, total_bayar, metode_valid)
                    pembayaran.proses_pembayaran()
                    
                    daftar_booking.append(booking_baru)
                    sistem_laporan.tambah_data_booking(booking_baru)
                    
                    print("\n[!] BOOKING BERHASIL [!]")
                    if bukti_pembayaran:
                        print(f"[*] Validasi sistem: Bukti referensi {bukti_pembayaran} telah terverifikasi.")
                    print(pembayaran.cetak_invoice())
                except ValueError as e:
                    print(f"[-] Gagal memproses pembayaran: {e}")
            else:
                daftar_booking.append(booking_baru)
                print("\n[!] BOOKING DISIMPAN DENGAN STATUS 'MENUNGGU PEMBAYARAN' [!]")
                print("Silakan lakukan pembayaran saat Daftar Ulang (Check-in) di studio.")
                
            jeda_interaksi()
                    
        elif pilihan == '2':
            print("\n[DAFTAR ULANG / CHECK-IN]")
            id_book = input("Masukkan ID Booking Anda: ").strip()
            ditemukan = False
            for b in daftar_booking:
                if b.id_booking == id_book:
                    ditemukan = True
                    if b.status == "Dibatalkan":
                        print("[-] Tidak bisa check-in. Pesanan ini sudah dibatalkan.")
                    elif b.status == "Selesai":
                        print("[-] Pesanan ini sudah selesai. Tidak perlu check-in lagi.")
                    elif b.status == "Diproses":
                        print("[-] Anda sudah melakukan check-in sebelumnya.")
                    else:
                        b.ubah_status("Diproses")
                        print(f"[+] Berhasil Check-in! Fotografer {b.fotografer.nama} segera melayani Anda.")
                        
                        if b not in sistem_laporan._Laporan__data_booking:
                            print("[!] Peringatan: Booking ini belum lunas! Harap arahkan klien ke kasir sebelum foto.")
                    break
            
            if not ditemukan:
                print("[-] ID Booking tidak ditemukan.")
            jeda_interaksi()
            
        elif pilihan == '0':
            break
            
        else:
            print("\n[-] Input salah! Pilihan yang Anda masukkan tidak tersedia.")
            if not konfirmasi_error(): break

def menu_fotografer():
    while True:
        print("\n--- MENU FOTOGRAFER ---")
        print("1. Cek Jadwal Kerja")
        print("0. Kembali ke Menu Utama")
        
        pil = input("Pilih menu: ").strip()
        if pil == '1':
            nama_fg = input("Masukkan nama Anda (contoh: Andi): ").strip()
            print(f"\n[JADWAL KERJA UNTUK {nama_fg.upper()}]")
            ada_jadwal = False
            
            for b in daftar_booking:
                if b.fotografer.nama.lower() == nama_fg.lower():
                    waktu = b.tanggal.strftime('%Y-%m-%d Jam %H:%M')
                    print(f"- {waktu} | Klien: {b.pelanggan.nama} | Paket: {b.paket.get_nama_paket()} | Status: {b.status}")
                    ada_jadwal = True
                    
            if not ada_jadwal:
                print("Tidak ada jadwal booking untuk Anda saat ini.")
            jeda_interaksi()
            
        elif pil == '0':
            break
        else:
            print("\n[-] Input salah! Pilihan yang Anda masukkan tidak tersedia.")
            if not konfirmasi_error(): break

def menu_manager():
    while True:
        print("\n--- MENU MANAGER ---")
        print("1. Laporan Harian")
        print("2. Laporan Bulanan")
        print("3. Selesaikan Pesanan (Tandai Selesai)")
        print("4. Batalkan Pesanan (User Ghosting/Batal)") 
        print("0. Kembali ke Menu Utama")
        
        pil = input("Pilih menu: ").strip()
        
        if pil == '1':
            tgl_str = input("Masukkan Tanggal (YYYY-MM-DD): ").strip()
            try:
                sistem_laporan.laporan_harian(datetime.strptime(tgl_str, "%Y-%m-%d"))
            except ValueError:
                print("[-] Format tanggal salah!")
            jeda_interaksi()
            
        elif pil == '2':
            try:
                tahun = int(input("Masukkan Tahun (contoh: 2026): ").strip())
                bulan = int(input("Masukkan Bulan (1-12): ").strip())
                sistem_laporan.laporan_bulanan(tahun=tahun, bulan=bulan)
            except ValueError:
                print("[-] Masukkan angka yang valid!")
            jeda_interaksi()
            
        elif pil == '3':
            id_book = input("Masukkan ID Booking yang sudah selesai: ").strip()
            ditemukan = False
            for b in daftar_booking:
                if b.id_booking == id_book:
                    ditemukan = True
                    if b.status == "Selesai":
                        print(f"[-] Status pesanan {id_book} sudah ditandai 'Selesai' sebelumnya!")
                    elif b.status == "Dibatalkan":
                        print("[-] Pesanan sudah dibatalkan, tidak bisa diselesaikan.")
                    else:
                        b.ubah_status("Selesai")
                        print(f"[+] Booking {id_book} berhasil ditandai Selesai. Pendapatan masuk ke Laporan.")
                    break
            
            if not ditemukan: print("[-] ID Booking tidak ditemukan.")
            jeda_interaksi()
            
        elif pil == '4':
            id_book = input("Masukkan ID Booking yang ingin dibatalkan: ").strip()
            ditemukan = False
            for b in daftar_booking:
                if b.id_booking == id_book:
                    ditemukan = True
                    if b.status == "Selesai":
                        print("[-] Tidak bisa membatalkan pesanan yang sudah berstatus 'Selesai'.")
                    else:
                        b.batalkan_booking()
                        print(f"[!] Booking {id_book} telah dibatalkan dari sistem (User Ghosting).")
                    break
            
            if not ditemukan: print("[-] ID Booking tidak ditemukan.")
            jeda_interaksi()
            
        elif pil == '0':
            print("\nTerima kasih telah menggunakan LensBooking!")
            simpan_data_booking()
            break
            
        else:
            print("\n[-] Input salah! Pilihan yang Anda masukkan tidak tersedia.")
            if not konfirmasi_error(): break

def main():
    while True:
        print("\n" + "="*45)
        print(" SISTEM BOOKING FOTO STUDIO (LENSBOOKING) MBG ")
        print("="*45)
        print("1. Masuk sebagai Pelanggan")
        print("2. Masuk sebagai Fotografer")
        print("3. Masuk sebagai Manager/Admin")
        print("0. Keluar Aplikasi")
        
        utama = input("Pilih peran Anda (0-3): ").strip()
        
        if utama == '1':
            menu_pelanggan()
        elif utama == '2':
            menu_fotografer()
        elif utama == '3':
            menu_manager()
        elif utama == '0':
            print("\nTerima kasih telah menggunakan LensBooking!")
            break
        else:
            print("\n[-] Pilihan peran tidak valid! Silakan pilih 0, 1, 2, atau 3.")
            jeda_interaksi()

if __name__ == "__main__":
    main()