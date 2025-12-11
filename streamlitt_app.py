import streamlit as st
import pandas as pd

# ==========================================
# BAGIAN 1: STRUKTUR OOP (MODEL)
# Sesuai Slide 6 (Class Planner)
# ==========================================

class Planner:
    """
    Merepresentasikan satu rencana perjalanan (Source: Slide 6)
    """
    def _init_(self, tujuan, tanggal, aktivitas):
        # Atribut Private (sesuai konvensi Python _var) - Source: Slide 6 (Atribut)
        self._tujuan = tujuan       # String, wajib ada
        self._tanggal = tanggal     # String, tidak boleh kosong
        self.aktivitas = aktivitas  # String, kegiatan utama

    # --- Getters & Setters (Source: Slide 6) ---
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

    def detail_text(self, qty_hari=1):
        """
        Menghasilkan ringkasan perjalanan.
        (Source: Slide 6 - detail_text())
        """
        return f"Trip ke {self._tujuan} pada {self._tanggal}. Aktivitas utama: {self.aktivitas}."

    def to_dict(self):
        """Helper untuk menampilkan data di Streamlit DataFrame"""
        return {
            "Tujuan": self._tujuan,
            "Tanggal": self._tanggal,
            "Aktivitas": self.aktivitas
        }

# ==========================================
# BAGIAN 2: LOGIC (MANAGEMENT)
# Sesuai Slide 7 (Class Management)
# ==========================================

class Management:
    """
    Bertugas mengelola kumpulan rencana perjalanan.
    (Source: Slide 7)
    """
    def _init_(self):
        # Atribut: daftar_rencana (list) - Source: Slide 7
        if 'daftar_rencana' not in st.session_state:
            st.session_state['daftar_rencana'] = []

    def tambah_rencana(self, rencana):
        """Create: Tambah aktivitas Trip (Source: Slide 4 & 7)"""
        st.session_state['daftar_rencana'].append(rencana)

    def lihat_semua(self):
        """Read: Melihat Trip Sebelumnya (Source: Slide 4 & 7)"""
        return st.session_state['daftar_rencana']

    def edit_rencana(self, index, rencana_baru):
        """Update: Edit trip yang sedang dijalani (Source: Slide 4 & 7)"""
        if 0 <= index < len(st.session_state['daftar_rencana']):
            st.session_state['daftar_rencana'][index] = rencana_baru

    def hapus_rencana(self, index):
        """Delete: Hapus rencana Trip (Source: Slide 4 & 7)"""
        if 0 <= index < len(st.session_state['daftar_rencana']):
            st.session_state['daftar_rencana'].pop(index)

# ==========================================
# BAGIAN 3: DATA LAYER (REPOSITORY)
# Sesuai Slide 8 & 9 (Class PlannerRepository)
# ==========================================

class PlannerRepository:
    """
    Bertugas sebagai pengelola data (Data Manager).
    Jembatan antara App dan Management.
    (Source: Slide 8)
    """
    def _init_(self):
        self.management = Management()

    def load_data(self):
        """Mengambil data (Source: Slide 9)"""
        # Dalam konteks Streamlit, data sudah ada di session_state via Management
        return self.management.lihat_semua()

    def save_data(self, planner_obj):
        """Menyimpan perubahan (Source: Slide 9)"""
        self.management.tambah_rencana(planner_obj)

    def get_planner(self):
        """Mengembalikan objek planner (Source: Slide 9)"""
        return self.management

# ==========================================
# BAGIAN 4: UI (APP)
# Sesuai Slide 10 (Class App)
# ==========================================

class App:
    """
    Main Class untuk menjalankan aplikasi.
    (Source: Slide 10)
    """
    def _init_(self):
        self.repo = PlannerRepository() # Atribut Planner Repository (Source: Slide 10)

    def run(self):
        """Menjalankan alur utama program (Source: Slide 10)"""
        st.set_page_config(page_title="EasyTrip Group 1", page_icon="✈")
        
        st.title("✈ EASYTRIP")
        
        self.tampilkan_menu()

    def tampilkan_menu(self):
        """Menampilkan menu interaksi (Source: Slide 10)"""
        # Menu sesuai Fitur CRUD di Slide 4
        menu = st.sidebar.selectbox(
            "Menu Utama",
            ["Create (Tambah Trip)", "Read (Lihat Trip)", "Update (Edit Trip)", "Delete (Hapus Trip)"]
        )
        
        self.proses_pilihan(menu)

    def proses_pilihan(self, menu):
        """Mengarahkan input user ke fungsi yang tepat (Source: Slide 10)"""
        
        # --- FITUR 1: CREATE (Source: Slide 4) ---
        if menu == "Create (Tambah Trip)":
            st.header("Tambah Rencana Baru")
            input_tujuan = st.text_input("Tujuan Destinasi")
            input_tanggal = st.date_input("Tanggal Perjalanan").strftime("%Y-%m-%d")
            input_aktivitas = st.text_area("Aktivitas Utama")
            
            if st.button("Simpan Rencana"):
                if input_tujuan and input_aktivitas:
                    # Membuat Objek Planner Baru (Source: Slide 6)
                    rencana_baru = Planner(input_tujuan, input_tanggal, input_aktivitas)
                    # Menyimpan via Repository (Source: Slide 8)
                    self.repo.save_data(rencana_baru)
                    st.success("Rencana perjalanan berhasil disimpan!")
                else:
                    st.error("Tujuan dan Aktivitas tidak boleh kosong!")

        # --- FITUR 2: READ (Source: Slide 4) ---
        elif menu == "Read (Lihat Trip)":
            st.header("Daftar Rencana Perjalanan")
            data_trip = self.repo.load_data()
            
            if not data_trip:
                st.info("Belum ada rencana perjalanan.")
            else:
                # Menampilkan data dalam bentuk Tabel
                list_data = [item.to_dict() for item in data_trip]
                st.table(pd.DataFrame(list_data))
                
                # Menampilkan detail text method dari Class Planner (Source: Slide 6)
                st.subheader("Detail Log:")
                for i, item in enumerate(data_trip):
                    st.text(f"{i+1}. {item.detail_text()}")

        # --- FITUR 3: UPDATE (Source: Slide 4) ---
        elif menu == "Update (Edit Trip)":
            st.header("Edit Rencana Perjalanan")
            data_trip = self.repo.load_data()
            
            if not data_trip:
                st.warning("Tidak ada data untuk diedit.")
                return

            # Pilih data berdasarkan index
            pilihan_index = st.selectbox("Pilih Trip untuk diedit", range(len(data_trip)), format_func=lambda x: data_trip[x].tujuan)
            objek_lama = data_trip[pilihan_index]

            st.write("--- Edit Data ---")
            # Form Edit
            edit_tujuan = st.text_input("Edit Tujuan", value=objek_lama.tujuan)
            edit_tanggal = st.text_input("Edit Tanggal (YYYY-MM-DD)", value=objek_lama.tanggal)
            edit_aktivitas = st.text_area("Edit Aktivitas", value=objek_lama.aktivitas)

            if st.button("Update Rencana"):
                # Update Objek Planner
                rencana_update = Planner(edit_tujuan, edit_tanggal, edit_aktivitas)
                # Panggil method edit di management
                self.repo.get_planner().edit_rencana(pilihan_index, rencana_update)
                st.success("Data berhasil diperbarui!")
                st.rerun()

        # --- FITUR 4: DELETE (Source: Slide 4) ---
        elif menu == "Delete (Hapus Trip)":
            st.header("Hapus Rencana Perjalanan")
            data_trip = self.repo.load_data()
            
            if not data_trip:
                st.warning("Tidak ada data untuk dihapus.")
                return

            # Pilih data berdasarkan index
            pilihan_index = st.selectbox("Pilih Trip untuk dihapus", range(len(data_trip)), format_func=lambda x: data_trip[x].tujuan)
            
            st.warning(f"Apakah Anda yakin ingin menghapus trip ke {data_trip[pilihan_index].tujuan}?")
            
            if st.button("Hapus Permanen"):
                # Panggil method hapus di management
                self.repo.get_planner().hapus_rencana(pilihan_index)
                st.success("Data berhasil dihapus.")
                st.rerun()

# ==========================================
# MAIN EXECUTION
# ==========================================
if __name__ == "__main__":
    app = App()
    app.run()


