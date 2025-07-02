import streamlit as st
from manajer_reservasi import SistemReservasi
from datetime import datetime

st.set_page_config(page_title="Reservasi Restoran", layout="centered")
sistem = SistemReservasi()

st.title("🍽️ Aplikasi Booking Kursi Restoran")

tab1, tab2, tab3 = st.tabs(["Lihat Meja", "Buat Reservasi", "Batalkan"])

# TAB 1 - Lihat semua meja
with tab1:
    st.header("Daftar Meja")
    for meja in sistem.daftar_meja:
        status = "✅ Tersedia" if meja.tersedia else "❌ Terisi"
        st.write(f"Meja {meja.nomor} (Kapasitas: {meja.kapasitas}) - {status}")

# TAB 2 - Buat reservasi
with tab2:
    st.header("Buat Reservasi")
    nama = st.text_input("Nama Pelanggan")
    jumlah = st.number_input("Jumlah Orang", min_value=1, step=1)
    tanggal = st.date_input("Pilih Tanggal Reservasi")
    jam_mulai = st.time_input("Pilih Jam Mulai (otomatis 2 jam)")

    # Filter meja berdasarkan kapasitas
    meja_opsi = [
        f"Meja {m.nomor} (Kapasitas {m.kapasitas})" 
        for m in sistem.daftar_meja if jumlah <= m.kapasitas
    ]
    if meja_opsi:
        meja_dipilih = st.selectbox("Pilih Meja", meja_opsi)
        nomor_meja = int(meja_dipilih.split()[1])
    else:
        nomor_meja = None
        st.warning("Tidak ada meja yang sesuai kapasitas.")

    if st.button("Reservasi"):
        if nama.strip() == "":
            st.warning("Nama tidak boleh kosong.")
        elif not nomor_meja:
            st.warning("Silakan pilih meja yang sesuai.")
        else:
            tanggal_str = tanggal.strftime("%Y-%m-%d")
            jam_str = jam_mulai.strftime("%H:%M")
            sukses = sistem.tambah_reservasi(nama, jumlah, tanggal_str, jam_str, nomor_meja)
            if sukses:
                st.success("Reservasi berhasil.")
                st.rerun()
            else:
                st.error("Reservasi gagal. Cek jadwal atau meja sudah dibooking.")

# TAB 3 - Batalkan reservasi
with tab3:
    st.header("Batalkan Reservasi")
    nama_batal = st.text_input("Masukkan Nama Pelanggan")
    if st.button("Batalkan"):
        if nama_batal.strip() == "":
            st.warning("Nama tidak boleh kosong.")
        else:
            berhasil = sistem.batalkan_reservasi(nama_batal)
            if berhasil:
                st.success("Reservasi berhasil dibatalkan.")
                st.rerun()
            else:
                st.error("Reservasi tidak ditemukan.")

# Tampilkan semua reservasi aktif
st.divider()
st.subheader("📋 Daftar Reservasi Saat Ini")
if sistem.daftar_reservasi:
    for r in sistem.daftar_reservasi:
        st.write("•", str(r))
else:
    st.write("Belum ada reservasi.")