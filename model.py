# model.py
from datetime import datetime

class Meja:
    def __init__(self, id, nomor, kapasitas, tersedia=True):
        self.id = id
        self.nomor = nomor
        self.kapasitas = kapasitas
        self.tersedia = tersedia

    def __str__(self):
        status = "Tersedia" if self.tersedia else "Terisi"
        return f"Meja {self.nomor} (Kapasitas: {self.kapasitas}) - {status}"

class Pelanggan:
    def __init__(self, id, nama, jumlah_orang):
        self.id = id
        self.nama = nama
        self.jumlah_orang = jumlah_orang

    def __str__(self):
        return f"{self.nama} ({self.jumlah_orang} orang)"

class Reservasi:
    def __init__(self, id, pelanggan, meja):
        self.id = id
        self.pelanggan = pelanggan
        self.meja = meja
        self.waktu = datetime.now()
        self.tanggal = None
        self.jam_mulai = None
        self.jam_selesai = None

    def __str__(self):
        if self.tanggal and self.jam_mulai and self.jam_selesai:
            return f"Reservasi oleh {self.pelanggan.nama} di Meja {self.meja.nomor} pada {self.tanggal} {self.jam_mulai}-{self.jam_selesai}"
        return f"Reservasi oleh {self.pelanggan.nama} di Meja {self.meja.nomor}"
