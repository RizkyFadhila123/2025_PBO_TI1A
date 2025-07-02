# manajer_reservasi.py
from model import Meja, Pelanggan, Reservasi
from datetime import datetime, timedelta
import database

class SistemReservasi:
    def __init__(self):
        self.refresh_data()

    def refresh_data(self):
        self.daftar_meja = self.ambil_semua_meja()
        self.daftar_reservasi = self.ambil_semua_reservasi()

    def ambil_semua_meja(self):
        rows = database.fetch_query("SELECT * FROM meja ORDER BY nomor")
        return [Meja(row['id'], row['nomor'], row['kapasitas'], row['tersedia']) for row in rows] if rows else []

    def ambil_semua_reservasi(self):
        rows = database.fetch_query("""
            SELECT r.id AS id, p.nama, p.jumlah_orang, m.nomor, m.kapasitas, r.tanggal, r.jam_mulai, r.jam_selesai
            FROM reservasi r
            JOIN pelanggan p ON r.pelanggan_id = p.id
            JOIN meja m ON r.meja_id = m.id
            ORDER BY r.id DESC
        """)
        if not rows:
            return []
        hasil = []
        for row in rows:
            pelanggan = Pelanggan(None, row['nama'], row['jumlah_orang'])
            meja = Meja(None, row['nomor'], row['kapasitas'], tersedia=False)
            reservasi = Reservasi(None, pelanggan, meja)
            reservasi.tanggal = row['tanggal']
            reservasi.jam_mulai = row['jam_mulai']
            reservasi.jam_selesai = row['jam_selesai']
            hasil.append(reservasi)
        return hasil

    def tampilkan_meja(self):
        print("\nDaftar Meja:")
        for meja in self.daftar_meja:
            print(meja)

    def hitung_jam_selesai(self, jam_mulai_str):
        jam_obj = datetime.strptime(jam_mulai_str, "%H:%M")
        jam_selesai = jam_obj + timedelta(hours=2)
        return jam_selesai.strftime("%H:%M")

    def tambah_reservasi(self, nama, jumlah_orang, tanggal, jam_mulai, nomor_meja):
        jam_selesai = self.hitung_jam_selesai(jam_mulai)

        meja = next((m for m in self.daftar_meja if m.nomor == nomor_meja), None)
        if not meja:
            print(f"❌ Meja nomor {nomor_meja} tidak ditemukan.")
            return False

        if jumlah_orang > meja.kapasitas:
            print(f"❌ Jumlah orang melebihi kapasitas Meja {meja.nomor}.")
            return False

        # Cek bentrok
        query = """
        SELECT * FROM reservasi
        WHERE meja_id = ? AND tanggal = ? AND NOT (
            ? <= jam_mulai OR ? >= jam_selesai
        )
        """
        bentrok = database.fetch_query(query, (
            meja.id, tanggal, jam_selesai, jam_mulai
        ))

        if bentrok:
            print(f"⚠️ Meja {meja.nomor} sudah dibooking di jam tersebut.")
            return False

        pelanggan_id = database.execute_query(
            "INSERT INTO pelanggan (nama, jumlah_orang) VALUES (?, ?)", (nama, jumlah_orang))
        if not pelanggan_id:
            print("❌ Gagal menambah pelanggan.")
            return False

        database.execute_query(
            "INSERT INTO reservasi (pelanggan_id, meja_id, tanggal, jam_mulai, jam_selesai) VALUES (?, ?, ?, ?, ?)",
            (pelanggan_id, meja.id, tanggal, jam_mulai, jam_selesai))

        database.execute_query(
            "UPDATE meja SET tersedia = 0 WHERE id = ?", (meja.id,))

        print(f"✅ Reservasi berhasil! {nama} di Meja {meja.nomor} pada {tanggal} {jam_mulai}-{jam_selesai}.")
        self.refresh_data()
        return True

    def batalkan_reservasi(self, nama):
        row = database.fetch_query("""
            SELECT r.id, r.meja_id, p.id AS pelanggan_id
            FROM reservasi r
            JOIN pelanggan p ON r.pelanggan_id = p.id
            WHERE p.nama = ?
            ORDER BY r.id DESC LIMIT 1
        """, (nama,), fetch_one=True)
        if not row:
            print("❌ Reservasi tidak ditemukan.")
            return False
        database.execute_query("DELETE FROM reservasi WHERE id = ?", (row['id'],))
        database.execute_query("DELETE FROM pelanggan WHERE id = ?", (row['pelanggan_id'],))
        database.execute_query("UPDATE meja SET tersedia = 1 WHERE id = ?", (row['meja_id'],))
        print(f"✅ Reservasi atas nama {nama} telah dibatalkan.")
        self.refresh_data()
        return True
