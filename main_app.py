# main_app.py
from manajer_reservasi import SistemReservasi

def menu():
    print("\n=== APLIKASI BOOKING KURSI RESTORAN ===")
    print("1. Lihat daftar meja")
    print("2. Tambah reservasi")
    print("3. Batalkan reservasi")
    print("4. Lihat semua reservasi")
    print("5. Keluar")

if __name__ == "__main__":
    sistem = SistemReservasi()
    while True:
        menu()
        pilihan = input("Pilih menu (1-5): ").strip()

        if pilihan == "1":
            sistem.tampilkan_meja()

        elif pilihan == "2":
            nama = input("Masukkan nama pelanggan: ")
            try:
                jumlah = int(input("Jumlah orang: "))
                tanggal = input("Tanggal (YYYY-MM-DD): ")
                jam_mulai = input("Jam mulai (HH:MM, contoh: 18:00): ")
                
                sistem.tampilkan_meja()
                nomor_meja = int(input("Pilih nomor meja: "))
                
                sistem.tambah_reservasi(nama, jumlah, tanggal, jam_mulai, nomor_meja)

            except ValueError:
                print("Jumlah dan nomor meja harus angka yang valid.")

        elif pilihan == "3":
            nama = input("Masukkan nama pelanggan yang ingin dibatalkan: ")
            sistem.batalkan_reservasi(nama)

        elif pilihan == "4":
            print("\nDaftar Reservasi Saat Ini:")
            if sistem.daftar_reservasi:
                for r in sistem.daftar_reservasi:
                    print("-", r)
            else:
                print("Belum ada reservasi.")

        elif pilihan == "5":
            print("Terima kasih telah menggunakan aplikasi ini.")
            break

        else:
            print("Pilihan tidak valid. Coba lagi.")