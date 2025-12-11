import streamlit as st
import pandas as pd
from datetime import datetime

# ==============================================================================
# BAGIAN 1: CLASS PLANNER (MODEL)
# Referensi: Slide 6 (Atribut, Setter/Getter, detail_text)
# ==============================================================================
class Planner:
    def _init_(self, tujuan, tanggal, aktivitas):
        # Atribut Private (Slide 6) [cite: 32-33]
        self._tujuan = tujuan
        self._tanggal = tanggal # Disimpan sebagai String sesuai Slide 6
        self.aktivitas = aktivitas

    # --- Getters & Setters (Slide 6) [cite: 27, 34-35] ---
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
        """Menghasilkan ringkasan perjalanan (Slide 6) [cite: 28, 36]"""
        return f"Perjalanan ke {self.tujuan} pada tanggal {self.tanggal}. Kegiatan: {self.aktivitas}."

    def to_dict(self):
        """Helper untuk mengubah objek menjadi data yang bisa dibaca DataFrame"""
        return {
            "Tujuan": self.tujuan,
            "Tanggal": self.tanggal,
            "Aktivitas": self.aktivitas
        }

# ==============================================================================
# BAGIAN 2: CLASS MANAGEMENT (LOGIC)
# Referensi: Slide 7 (Mengelola kumpulan rencana)
# ==============================================================================
class Management:
    def _init_(self):
        # Inisialisasi list penyimpanan di Session State agar data AWET (Persistent)
        # Ini implementasi dari 'Daftar_rencana' (Slide 7) [cite: 40, 47]
        if 'daftar_rencana' not in st.session_state:
            st.session_state['daftar_rencana'] = []

    def tambah_rencana(self, rencana):
        """Create: Menambahkan rencana (Slide 7) [cite: 41, 49]"""
        st.session_state['daftar_rencana'].append(rencana)

    def lihat_semua(self):
        """Read: Menampilkan seluruh rencana (Slide 7) [cite: 42, 51]"""
        return st.session_state['daftar_rencana']

    def edit_rencana(self, index, rencana_baru):
        """Update: Mengedit rencana berdasarkan index (Slide 7) [cite: 43, 52]"""
        if 0 <= index < len(st.session_state['daftar_rencana']):
            st.session_state['daftar_rencana'][index] = rencana_baru

    def hapus_rencana(self, index):
        """Delete: Menghapus rencana tertentu (Slide 7) [cite: 44, 53]"""
        if 0 <= index < len(st.session_state['daftar_rencana']):
            st.session_state['daftar_rencana'].pop(index)

# ==============================================================================
# BAGIAN 3: CLASS PLANNER REPOSITORY (DATA LAYER)
# Referensi: Slide 8-9 (Jembatan antara App dan Management)
# ==============================================================================
class PlannerRepository:
    def _init_(self):
        # Repository memiliki atribut management (Slide 9) [cite: 72]
        self.management = Management()

    def load_data(self):
        """Mengambil data (Slide 8 & 9) [cite: 58, 73]"""
        return self.management.lihat_semua()

    def save_data(self, planner_obj):
        """Menyimpan data (Slide 8 & 9) [cite: 59, 74]"""
        self.management.tambah_rencana(planner_obj)

    def get_planner(self):
        """Mengakses objek management (Slide 8 & 9) [cite: 60, 75]"""
        return self.management

# ==============================================================================
# BAGIAN 4: CLASS APP (UI / TAMPILAN)
# Referensi: Slide 10 (Menu, Run, Input User)
# ==============================================================================
class App:
    def _init_(self):
        # Atribut Planner Repository sebagai sumber data (Slide 10) [cite: 78]
        self.repo = PlannerRepository()

    def run(self):
        """Menjalankan alur utama program (Slide 10) [cite: 80]"""
        st.set_page_config(page_title="EasyTrip Planner", page_icon="✈", layout="wide")
        
        # Header Tampilan
        st.title("✈ EasyTrip: Trip Planner")
        st.markdown("Aplikasi Perencanaan Perjalanan Sederhana Berbasis Python (Kelompok 1)")
        st.write("---")

        self.tampilkan_menu()

    def tampilkan_menu(self):
        """Menampilkan menu interaksi (Slide 10) [cite: 81]"""
        with st.sidebar:
            st.header("Menu Navigasi")
            # Pilihan menu sesuai 4 operasi dasar CRUD (Slide 4) [cite: 14]
            pilihan = st.radio(
                "Pilih Aksi:",
                ["1. Create (Tambah Trip)", 
                 "2. Read (Lihat Trip)", 
                 "3. Update (Edit Trip)", 
                 "4. Delete (Hapus Trip)"]
            )
        
        self.proses_pilihan(pilihan)

    def proses_pilihan(self, pilihan):
        """Logika untuk memproses input user (Slide 10) [cite: 83]"""
        
        # --- FITUR CREATE (Tambah) ---
        if "Create" in pilihan:
            st.subheader("📝 Tambah Rencana Perjalanan Baru")
            with st.form("form_tambah"):
                in_tujuan = st.text_input("Tujuan Destinasi")
                in_tanggal = st.date_input("Tanggal Keberangkatan")
                in_aktivitas = st.text_area("Aktivitas Utama")
                submit_btn = st.form_submit_button("Simpan Rencana")

                if submit_btn:
                    if in_tujuan and in_aktivitas:
                        # Konversi tanggal ke string agar sesuai atribut di Slide 6
                        tgl_str = in_tanggal.strftime("%Y-%m-%d")
                        # Buat Objek Planner
                        obj_baru = Planner(in_tujuan, tgl_str, in_aktivitas)
                        # Simpan lewat Repository
                        self.repo.save_data(obj_baru)
                        st.success(f"Berhasil menyimpan trip ke {in_tujuan}!")
                    else:
                        st.error("Mohon isi semua data (Tujuan & Aktivitas).")

        # --- FITUR READ (Lihat) ---
        elif "Read" in pilihan:
            st.subheader("📋 Daftar Rencana Perjalanan Anda")
            data = self.repo.load_data()
            
            if not data:
                st.info("Belum ada data trip. Silakan tambah data baru di menu Create.")
            else:
                # Tampilan Tabel Rapi
                list_dict = [item.to_dict() for item in data]
                st.dataframe(pd.DataFrame(list_dict), use_container_width=True)
                
                # Tampilan Detail Text (Sesuai method di Slide 6)
                with st.expander("Lihat Detail Deskripsi (Method OOP)"):
                    for i, item in enumerate(data):
                        st.write(f"*Trip #{i+1}:* {item.detail_text()}")

        # --- FITUR UPDATE (Edit) ---
        elif "Update" in pilihan:
            st.subheader("✏ Edit Rencana Perjalanan")
            data = self.repo.load_data()
            
            if not data:
                st.warning("Tidak ada data untuk diedit.")
            else:
                # Pilih data berdasarkan nama tujuan
                list_nama = [f"{i+1}. {item.tujuan} ({item.tanggal})" for i, item in enumerate(data)]
                pilihan_index = st.selectbox("Pilih Trip yang mau diedit:", range(len(data)), format_func=lambda x: list_nama[x])
                
                trip_lama = data[pilihan_index]
                
                st.write("---")
                with st.form("form_edit"):
                    edit_tujuan = st.text_input("Edit Tujuan", value=trip_lama.tujuan)
                    # Konversi string tanggal kembali ke object date untuk default value picker
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
                        
                        # Update lewat Repository -> Management
                        self.repo.get_planner().edit_rencana(pilihan_index, trip_baru)
                        st.success("Data berhasil diperbarui! Silakan cek menu Read.")
                        st.rerun() # Refresh halaman otomatis

        # --- FITUR DELETE (Hapus) ---
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

