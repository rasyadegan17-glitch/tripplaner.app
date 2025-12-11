import streamlit as st
import pandas as pd
from datetime import date, timedelta

# ==========================================
# BAGIAN 1: STRUKTUR OOP (MODEL & LOGIC)
# Mengacu pada konsep Class Planner  dan Management 
# ==========================================

class TransportBooking:
    """
    Parent Class (Kelas Induk).
    Menyimpan atribut dasar transportasi sesuai dokumen PDF (Planner).
    """
    def _init_(self, booking_type, sub_type):
        self.booking_type = booking_type # e.g., Pesawat
        self.sub_type = sub_type         # e.g., Domestik
        self.origin = ""
        self.destination = ""
        self.depart_date = date.today()
        self.return_date = None
        self.passengers = 1

    def set_details(self, origin, destination, dates, passengers):
        """Setter untuk mengisi data perjalanan [cite: 27]"""
        self.origin = origin
        self.destination = destination
        self.passengers = passengers
        
        # Logika menangani tanggal (sekali jalan vs pulang pergi)
        if isinstance(dates, tuple) and len(dates) == 2:
            self.depart_date = dates[0]
            self.return_date = dates[1]
        elif isinstance(dates, tuple) and len(dates) == 1:
            self.depart_date = dates[0]
            self.return_date = None
        else:
            self.depart_date = dates
            self.return_date = None

    def to_dict(self):
        """Helper untuk mengubah objek menjadi dictionary (untuk DataFrame)"""
        tgl = f"{self.depart_date}"
        if self.return_date:
            tgl += f" - {self.return_date}"
        
        return {
            "Jenis": self.booking_type,
            "Tipe": self.sub_type,
            "Rute": f"{self.origin} -> {self.destination}",
            "Tanggal": tgl,
            "Penumpang": self.passengers
        }

class BookingManager:
    """
    Class Management 
    Bertugas mengelola kumpulan rencana perjalanan (CRUD).
    """
    def _init_(self):
        # Menggunakan Session State agar data tidak hilang saat reload
        if 'bookings' not in st.session_state:
            st.session_state['bookings'] = []

    def add_booking(self, booking_obj):
        """Fitur Create: Menambah aktivitas Trip [cite: 15]"""
        st.session_state['bookings'].append(booking_obj)

    def get_all_bookings(self):
        """Fitur Read: Melihat Trip Sebelumnya [cite: 16]"""
        return st.session_state['bookings']
    
    def delete_booking(self, index):
        """Fitur Delete: Hapus rencana Trip [cite: 18]"""
        if 0 <= index < len(st.session_state['bookings']):
            st.session_state['bookings'].pop(index)

# ==========================================
# BAGIAN 2: UI & LOGIC (VIEW CONTROLLER)
# Mengacu pada Class App 
# ==========================================

class TravelAppUI:
    """Class untuk mengatur Tampilan Antarmuka Streamlit"""
    
    def _init_(self):
        self.manager = BookingManager() # Inisialisasi Manager
        self.apply_custom_style()

    def apply_custom_style(self):
        """Menambahkan CSS untuk background Orange Gradiasi & Style Traveloka"""
        st.markdown(
            """
            <style>
            .stApp {
                background: linear-gradient(to right, #00C6FB, #005BEA); /* Biru Traveloka */
                background: linear-gradient(to right, #ff7e5f, #feb47b); /* Request User: Oren */
                color: black;
            }
            /* Styling Tab agar terlihat rapi */
            .stTabs [data-baseweb="tab-list"] {
                gap: 10px;
                background-color: rgba(255,255,255, 0.2);
                padding: 10px;
                border-radius: 10px;
            }
            .stTabs [data-baseweb="tab"] {
                background-color: white;
                border-radius: 5px;
                padding: 10px 20px;
                color: #ff7e5f;
                font-weight: bold;
            }
            .stTabs [aria-selected="true"] {
                background-color: #e65100 !important;
                color: white !important;
            }
            /* Styling Container form input */
            div[data-testid="stVerticalBlockBorderWrapper"] {
                background-color: rgba(255, 255, 255, 0.95);
                border-radius: 10px;
                padding: 20px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }
            </style>
            """,
            unsafe_allow_html=True
        )

    def render_common_inputs(self, key_prefix):
        """
        Input form standar (Asal, Tujuan, Tanggal, Penumpang).
        Digunakan ulang untuk semua tab (DRY Principle).
        """
        col1, col2 = st.columns(2)
        with col1:
            origin = st.text_input("Dari", placeholder="Asal (e.g. Jakarta)", key=f"{key_prefix}_org")
        with col2:
            dest = st.text_input("Ke", placeholder="Tujuan (e.g. Bali)", key=f"{key_prefix}_dest")

        col3, col4 = st.columns(2)
        with col3:
            travel_dates = st.date_input(
                "Tanggal Pergi & Pulang",
                (date.today(), date.today() + timedelta(days=3)),
                key=f"{key_prefix}_date"
            )
        with col4:
            passengers = st.number_input("Jumlah Penumpang", min_value=1, max_value=10, value=1, key=f"{key_prefix}_pax")

        return origin, dest, travel_dates, passengers

    def run(self):
        """Fungsi Utama (Main Loop) [cite: 78]"""
        
        # Header Aplikasi
        col_logo, col_title = st.columns([1, 5])
        with col_title:
            st.title("🕊 TravelPlanner")
            st.markdown("### Pilihan utama untuk jelajahi dunia")

        # Tab Navigasi Utama (Pesawat, Kereta, Bus, Riwayat)
        tab_pesawat, tab_kereta, tab_bus, tab_history = st.tabs(
            ["✈ Tiket Pesawat", "🚆 Tiket Kereta Api", "🚌 Bus & Travel", "📜 Pesanan Saya"]
        )

        # --- TAB 1: PESAWAT ---
        with tab_pesawat:
            with st.container(border=True):
                st.subheader("Cari Penerbangan")
                flight_type = st.radio("Tipe:", ["Domestic", "International"], horizontal=True)
                st.divider()
                origin, dest, dates, pax = self.render_common_inputs("flight")
                
                if st.button("Cari & Pesan Pesawat", type="primary"):
                    booking = TransportBooking("Pesawat", flight_type)
                    booking.set_details(origin, dest, dates, pax)
                    self.manager.add_booking(booking) # Simpan ke Management [cite: 49]
                    st.success("Berhasil ditambahkan ke Pesanan Saya!")

        # --- TAB 2: KERETA API ---
        with tab_kereta:
            with st.container(border=True):
                st.subheader("Cari Kereta Api")
                train_type = st.radio("Kelas:", ["Ekonomi", "Bisnis", "Eksekutif", "Luxury"], horizontal=True)
                st.divider()
                origin, dest, dates, pax = self.render_common_inputs("train")
                
                if st.button("Cari & Pesan Kereta", type="primary"):
                    booking = TransportBooking("Kereta Api", train_type)
                    booking.set_details(origin, dest, dates, pax)
                    self.manager.add_booking(booking)
                    st.success("Berhasil ditambahkan ke Pesanan Saya!")

        # --- TAB 3: BUS & TRAVEL ---
        with tab_bus:
            with st.container(border=True):
                st.subheader("Cari Bus & Travel")
                bus_type = st.radio("Tipe:", ["Bus Malam", "Shuttle DayTrans", "Airport Transfer"], horizontal=True)
                st.divider()
                origin, dest, dates, pax = self.render_common_inputs("bus")
                
                if st.button("Cari & Pesan Bus", type="primary"):
                    booking = TransportBooking("Bus & Travel", bus_type)
                    booking.set_details(origin, dest, dates, pax)
                    self.manager.add_booking(booking)
                    st.success("Berhasil ditambahkan ke Pesanan Saya!")

        # --- TAB 4: PESANAN SAYA (Fitur Read/Delete PDF) [cite: 16, 18] ---
        with tab_history:
            st.subheader("Daftar Rencana Perjalanan")
            all_bookings = self.manager.get_all_bookings()
            
            if not all_bookings:
                st.info("Belum ada pesanan. Silakan pesan tiket di tab lain.")
            else:
                # Menampilkan Data dalam Tabel
                data_list = [b.to_dict() for b in all_bookings]
                df = pd.DataFrame(data_list)
                st.dataframe(df, use_container_width=True)

                st.divider()
                # Fitur Hapus [cite: 53]
                st.write("Kelola Pesanan:")
                col_del1, col_del2 = st.columns([3, 1])
                with col_del1:
                    idx_to_del = st.number_input("Pilih Index (Baris) untuk dihapus", min_value=0, max_value=len(all_bookings)-1 if len(all_bookings)>0 else 0, step=1)
                with col_del2:
                    if st.button("Hapus Pesanan"):
                        self.manager.delete_booking(idx_to_del)
                        st.rerun()

# ==========================================
# EKSEKUSI PROGRAM
# ==========================================
if __name__ == "__main__":
    app = TravelAppUI()
    app.run()
