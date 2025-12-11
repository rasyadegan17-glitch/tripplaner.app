import streamlit as st
import pandas as pd
from datetime import datetime

# ==============================================================================
# BAGIAN 1: CLASS PLANNER (MODEL)
# ==============================================================================
class Planner:
    # PERBAIKAN PENTING: Gunakan _init_ (double underscore)
    def _init_(self, tujuan, tanggal, aktivitas):
        self._tujuan = tujuan
        self._tanggal = tanggal
        self.aktivitas = aktivitas

    # --- Getters & Setters ---
    @property
    def tujuan(self):
        return self._tujuan

    @tujuan.setter
    def tujuan(self, value):
        if value:
            self._tujuan = value

    @property
    def tanggal(self):
        return self._tanggal

    @tanggal.setter
    def tanggal(self, value):
        if value:
            self._tanggal = value

    def detail_text(self):
        # Method untuk menampilkan detail text sesuai Slide 6
        return f"Perjalanan ke {self.tujuan} pada tanggal {self.tanggal}. Kegiatan: {self.aktivitas}."

    def to_dict(self):
        return {
            "Tujuan": self.tujuan,
            "Tanggal": self.tanggal,
            "Aktivitas": self.aktivitas
        }

# ==============================================================================
# BAGIAN 2: CLASS MANAGEMENT (LOGIC)
# ==============================================================================
class Management:
    # PERBAIKAN PENTING: Gunakan _init_ (double underscore)
    def _init_(self):
        # Menggunakan Session State agar data tersimpan saat tombol ditekan
        if 'daftar_rencana' not in st.session_state:
            st.session_state['daftar_rencana'] = []

    def tambah_rencana(self, rencana):
        st.session_state['daftar_rencana'].append(rencana)

    def lihat_semua(self):
        return st.session_state['daftar_rencana']

    def edit_rencana(self, index, rencana_baru):
        if 0 <= index < len(st.session_state['daftar_rencana']):
            st.session_state['daftar_rencana'][index] = rencana_baru

    def hapus_rencana(self, index):
        if 0 <= index < len(st.session_state['daftar_rencana']):
            st.session_state['daftar_rencana'].pop(index)

# ==============================================================================
# BAGIAN 3: CLASS PLANNER REPOSITORY (DATA LAYER)
# ==============================================================================
class PlannerRepository:
    # PERBAIKAN PENTING: Gunakan _init_ (double underscore)
    def _init_(self):
        self.management = Management()

    def load_data(self):
        return self.management.lihat_semua()

    def save_data(self, planner_obj):
        self.management.tambah_rencana(planner_obj)

    def get_planner(self):
        return self.management

# ==============================================================================
# BAGIAN 4: CLASS APP (UI / TAMPILAN)
# ==============================================================================
class App:
    # PERBAIKAN PENTING: Gunakan _init_ (double underscore)
    def _init_(self):
        self.repo = PlannerRepository()

    def run(self):
        st.set_page_config(page_title="EasyTrip Planner", page_icon="✈", layout="wide")
        
        st.title("✈ EasyTrip: Trip Planner")
        st.markdown("Aplikasi Perencanaan Perjalanan Sederhana Berbasis Python (Kelompok 1)")
        st.write("---")

        self.tampilkan_menu()

    def tampilkan_menu(self):
        with st.sidebar:
            st.header("Menu Navigasi")
            # Menu sesuai CRUD dasar
            pilihan = st.radio(
                "Pilih Aksi:",
                ["1. Create (Tambah Trip)", 
                 "2. Read (Lihat Trip)", 
                 "3. Update (Edit Trip)", 
                 "4. Delete (Hapus Trip)"]
            )
        
        self.proses_pilihan(pilihan)

    def proses_pilihan(self, pilihan):
        # --- FITUR CREATE (Input Data) ---
        if "Create" in pilihan:
            st.subheader("📝 Tambah Rencana Perjalanan Baru")
            
            # Form Input
            with st.form("form_tambah"):
                in_tujuan = st.text_input("Tujuan Destinasi")
                in_tanggal = st.date_input("Tanggal Keberangkatan")
                in_aktivitas = st.text_area("Aktivitas Utama")
                submit_btn = st.form_submit_button("Simpan Rencana")

                if submit_btn:
                    if in_tujuan and in_aktivitas:
                        try:
                            tgl_str = in_tanggal.strftime("%Y-%m-%d")
                            
                            # DISINI ERROR ANDA SEBELUMNYA TERJADI
                            # Sekarang sudah aman karena _init_ di class Planner sudah benar
                            obj_baru = Planner(in_tujuan, tgl_str, in_aktivitas)
                            
                            self.repo.save_data(obj_baru)
                            st.success(f"Berhasil menyimpan trip ke {in_tujuan}!")
                        except Exception as e:
                            st.error(f"Terjadi kesalahan: {e}")
                    else:
                        st.error("Mohon isi semua data (Tujuan & Aktivitas).")

        # --- FITUR READ (Lihat Data) ---
        elif "Read" in pilihan:
            st.subheader("📋 Daftar Rencana Perjalanan Anda")
            data = self.repo.load_data()
            
            if not data:
                st.info("Belum ada data trip. Silakan tambah data baru di menu Create.")
            else:
                # Menampilkan Tabel
                list_dict = [item.to_dict() for item in data]
                st.dataframe(pd.DataFrame(list_dict), use_container_width=True)
                
                # Menampilkan Detail Text
                with st.expander("Lihat Detail Deskripsi (Method OOP)"):
                    for i, item in enumerate(data):
                        st.write(f"*Trip #{i+1}:* {item.detail_text()}")

        # --- FITUR UPDATE (Edit Data) ---
        elif "Update" in pilihan:
            st.subheader("✏ Edit Rencana Perjalanan")
            data = self.repo.load_data()
            
            if not data:
                st.warning("Tidak ada data untuk diedit.")
            else:
                list_nama = [f"{i+1}. {item.tujuan} ({item.tanggal})" for i, item in enumerate(data)]
                pilihan_index = st.selectbox("Pilih Trip yang mau diedit:", range(len(data)), format_func=lambda x: list_nama[x])
                
                trip_lama = data[pilihan_index]
                
                st.write("---")
                with st.form("form_edit"):
                    edit_tujuan = st.text_input("Edit Tujuan", value=trip_lama.tujuan)
                    
                    # Handling konversi tanggal untuk default value
                    try:
                        def_date = datetime.strptime(trip_lama.tanggal, "%Y-%m-%d").date()
                    except:
                        def_date = datetime.today()
                        
                    edit_tanggal = st.date_input("Edit Tanggal", value=def_date)
                    edit_aktivitas = st.text_area("Edit Aktivitas", value=trip_lama.aktivitas)
                    
                    update_btn = st.form_submit_button("Update Data")
                    
                    if update_btn:
                        tgl_str_baru = edit_tanggal.strftime("%Y-%m-%d")
                        trip_baru = Planner(edit_tujuan, tgl_str_baru, edit_aktivitas)
                        
                        self.repo.get_planner().edit_rencana(pilihan_index, trip_baru)
                        st.success("Data berhasil diperbarui! Silakan cek menu Read.")
                        st.rerun()

        # --- FITUR DELETE (Hapus Data) ---
        elif "Delete" in pilihan:
            st.subheader("🗑 Hapus Rencana Perjalanan")
            data = self.repo.load_data()
            
            if not data:
                st.warning("Tidak ada data untuk dihapus.")
            else:
                list_nama = [f"{i+1}. {item.tujuan} ({item.tanggal})" for i, item in enumerate(data)]
                idx_hapus = st.selectbox("Pilih Trip yang mau dihapus:", range(len(data)), format_func=lambda x: list_nama[x])
                
                st.write(f"Anda akan menghapus: *{data[idx_hapus].detail_text()}*")
                
                if st.button("Hapus Permanen", type="primary"):
                    self.repo.get_planner().hapus_rencana(idx_hapus)
                    st.success("Data telah dihapus.")
                    st.rerun()

# ==============================================================================
# MAIN PROGRAM
# ==============================================================================
if __name__ == "__main__":
    app = App()
    app.run()


