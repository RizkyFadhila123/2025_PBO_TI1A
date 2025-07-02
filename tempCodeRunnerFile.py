# setup_db.py
import sqlite3
from konfigurasi import DB_PATH, JUMLAH_MEJA, KAPASITAS_DEFAULT

def setup_database():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS meja (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nomor INTEGER NOT NULL UNIQUE,
            kapasitas INTEGER NOT NULL,
            tersedia BOOLEAN NOT NULL DEFAULT 1
        );
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS pelanggan (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            jumlah_orang INTEGER NOT NULL
        );
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS reservasi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pelanggan_id INTEGER NOT NULL,
            meja_id INTEGER NOT NULL,
            tanggal TEXT NOT NULL,
            jam_mulai TEXT NOT NULL,
            jam_selesai TEXT NOT NULL,
            FOREIGN KEY (pelanggan_id) REFERENCES pelanggan(id),
            FOREIGN KEY (meja_id) REFERENCES meja(id)
        );
        """)

        cursor.execute("SELECT COUNT(*) FROM meja")
        if cursor.fetchone()[0] == 0:
            for i in range(1, JUMLAH_MEJA + 1):
                cursor.execute("INSERT INTO meja (nomor, kapasitas) VALUES (?, ?)", (i, KAPASITAS_DEFAULT))

        conn.commit()
        print("Database berhasil disiapkan.")
    except sqlite3.Error as e:
        print(f"Gagal setup database: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    setup_database()
