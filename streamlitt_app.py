import streamlit as st
from datetime import date, timedelta

# ==========================================
# BAGIAN 1: STRUKTUR OOP (MODEL)
# ==========================================

class TransportBooking:
    """
    Parent Class (Kelas Induk).
    Menyimpan atribut dasar yang dimiliki semua jenis transportasi.
    """
    def _init_(self, booking_type, sub_type):
        # Perhatikan: _init_ menggunakan DUA garis bawah di kiri dan kanan
        self.booking_type = booking_type # e.g., Pesawat
        self.sub_type = sub_type         # e.g., Domestik
        self.origin = ""
        self.destination = ""
        self.depart_date = date.today()
        self.return_date = None
        self.passengers = 1

    def set_details(self, origin, destination, dates, passengers):
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

    def display_ticket_summary(self):
        """Method untuk menampilkan hasil booking"""
        st.success(f"✅ Tiket {self.booking_type} ({self.sub_type}) Berhasil Dipesan!")
        st.write(f"*Rute:* {self.origin} ➡ {self.destination}")
        
        date_str = f"{self.depart_date}"
        if self.return_date:
            date_str += f" s/d {self.return_date}"
            
        st.write(f"*Tanggal:* {date_str}")
        st.write(f"*Penumpang:* {self.passengers} Orang")

# ==========================================
# BAGIAN 2: UI & LOGIC (VIEW CONTROLLER)
# ==========================================

class TravelAppUI:
    """Class untuk mengatur Tampilan Antarmuka Streamlit"""
    
    def _init_(self):
        # Inisialisasi tampilan saat class dipanggil
        self.apply_custom_style()

    def apply_custom_style(self):
        """Menambahkan CSS untuk background Orange Gradiasi"""
        st.markdown(
            """
            <style>
            .stApp {
                background: linear-gradient(to right, #ff7e5f, #feb47b);
                color: black;
            }
            /* Styling Tab agar terlihat rapi di background oranye */
            .stTabs [data-baseweb="tab-list"] {
                gap: 10px;
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
            div[data-testid="stExpander"], div[data-testid="stVerticalBlockBorderWrapper"] {
                background-color: rgba(255, 255, 255, 0.9);
                border-radius: 10px;
                padding: 20px;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

    def render_common_inputs(self, key_prefix):
        """
        Input form standar (DRY Principle).
        Mencegah penulisan ulang kode untuk input Asal, Tujuan, Tanggal.
        """
        col1, col2 = st.columns(2)
        with col1:
            origin = st.text_input("Dari (Kota Asal)", placeholder="Contoh: Jakarta", key=f"{key_prefix}_org")
        with col2:
            dest = st.text_input("Ke (Kota Tujuan)", placeholder="Contoh: Singapura", key=f"{key_prefix}_dest")

        col3, col4 = st.columns(2)
        with col3:
            travel_dates = st.date_input(
                "Tanggal Pergi & Pulang",
                (date.today(), date.today() + timedelta(days=3)),
                key=f"{key_prefix}_date"
            )
            st.caption("*Pilih rentang tanggal untuk Pulang-Pergi")
        with col4:
            passengers = st.number_input("Jumlah Penumpang", min_value=1, max_value=10, value=1, key=f"{key_prefix}_pax")

        return origin, dest, travel_dates, passengers

    def run(self):
        """Fungsi Utama untuk menjalankan aplikasi"""
        st.title("🌏 Trip Planner App")
        st.markdown("### Pilihan utama untuk jelajahi dunia")

        # Tab Navigasi Utama
        tab_pesawat, tab_kereta, tab_bus = st.tabs(["✈ Tiket Pesawat", "🚆 Tiket Kereta Api", "🚌 Tiket Bus & Travel"])

        # --- TAB 1: PESAWAT ---
        with tab_pesawat:
            with st.container():
                st.markdown("#### Pengaturan Penerbangan")
                flight_type = st.radio("Tipe Penerbangan:", ["Domestic", "International"], horizontal=True)
                
                st.divider()
                origin, dest, dates, pax = self.render_common_inputs("flight")
                
                if st.button("Cari Penerbangan", type="primary"):
                    booking = TransportBooking("Pesawat", flight_type)
                    booking.set_details(origin, dest, dates, pax)
                    st.divider()
                    booking.display_ticket_summary()

        # --- TAB 2: KERETA API ---
        with tab_kereta:
            with st.container():
                st.markdown("#### Pengaturan Kereta")
                train_type = st.radio("Tipe Kereta:", ["Whoosh", "Intercity", "Airport"], horizontal=True)
                
                st.divider()
                origin, dest, dates, pax = self.render_common_inputs("train")
                
                if st.button("Cari Kereta Api", type="primary"):
                    booking = TransportBooking("Kereta Api", train_type)
                    booking.set_details(origin, dest, dates, pax)
                    st.divider()
                    booking.display_ticket_summary()

        # --- TAB 3: BUS & TRAVEL ---
        with tab_bus:
            with st.container():
                st.markdown("#### Pengaturan Bus & Shuttle")
                bus_type = st.radio("Tipe Bus:", ["Airport", "Shuttle"], horizontal=True)
                
                st.divider()
                origin, dest, dates, pax = self.render_common_inputs("bus")
                
                if st.button("Cari Bus / Travel", type="primary"):
                    booking = TransportBooking("Bus & Travel", bus_type)
                    booking.set_details(origin, dest, dates, pax)
                    st.divider()
                    booking.display_ticket_summary()

# ==========================================
# EKSEKUSI PROGRAM
# ==========================================
if __name__ == "_main_":
    app = TravelAppUI()
    app.run()

