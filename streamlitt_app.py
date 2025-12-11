import streamlit as st
from dataclasses import dataclass, field
from typing import List

# ============================================
#             MODERN OOP (DATACLASS)
# ============================================

@dataclass
class Activity:
    name: str
    cost: int
    duration: float

@dataclass
class Destination:
    name: str
    location: str
    activities: List[Activity] = field(default_factory=list)

    def total_cost(self):
        # Mengembalikan total biaya semua aktivitas di destinasi ini
        return sum(a.cost for a in self.activities)

@dataclass
class Trip:
    trip_id: str
    title: str
    destinations: List[Destination] = field(default_factory=list)

    def total_cost(self):
        # Mengembalikan total biaya semua destinasi (dan aktivitasnya) di trip ini
        return sum(d.total_cost() for d in self.destinations)

# ============================================
#             MAIN APP LOGIC
# ============================================

st.set_page_config(layout="wide") # Menggunakan layout lebar
st.title("✈ Trip Planner Sat-Set (Mode 1 Halaman)")
st.caption("Semua fitur ada di tab di bawah.")

# 1. State Management (Inisialisasi data di memori)
if "trips" not in st.session_state:
    st.session_state.trips = []

# 2. Layout dengan Tabs
tab1, tab2, tab3, tab4 = st.tabs(
    ["➕ Buat Trip", "🏝 Tambah Destinasi", "🎯 Tambah Aktivitas", "📋 Lihat Rangkuman"]
)

# --- TAB 1: BUAT TRIP BARU ---
with tab1:
    st.subheader("1. Buat Trip Baru")
    with st.form("new_trip"):
        c1, c2 = st.columns(2)
        tid = c1.text_input("ID Unik Trip (Contoh: Bali2026)")
        ttl = c2.text_input("Nama Trip (Contoh: Liburan Keluarga ke Bali)")
        
        if st.form_submit_button("Simpan Trip") and tid and ttl:
            if any(t.trip_id == tid for t in st.session_state.trips):
                 st.error("ID Trip sudah ada. Gunakan ID unik lain.")
            else:
                st.session_state.trips.append(Trip(tid, ttl))
                st.success(f"Trip '{ttl}' berhasil dibuat!")

# --- TAB 2: TAMBAH DESTINASI ---
with tab2:
    st.subheader("2. Tambah Destinasi ke Trip")
    
    if not st.session_state.trips:
        st.warning("⚠ Belum ada Trip yang dibuat. Silakan ke Tab 'Buat Trip'.");
    else:
        # Pilihan Trip
        trip = st.selectbox("Pilih Trip Tujuan", st.session_state.trips, format_func=lambda t: t.title, key='select_trip_dest')
        
        st.markdown("---")
        with st.form("add_dest"):
            c1, c2 = st.columns(2)
            name = c1.text_input("Nama Tempat / Destinasi")
            loc = c2.text_input("Lokasi / Kota Destinasi")
            
            if st.form_submit_button("Tambah Destinasi") and name:
                trip.destinations.append(Destination(name, loc))
                st.success(f"Destinasi '{name}' berhasil ditambahkan ke {trip.title}!")

# --- TAB 3: TAMBAH AKTIVITAS ---
with tab3:
    st.subheader("3. Tambah Aktivitas ke Destinasi")

    if not st.session_state.trips:
        st.warning("⚠ Belum ada Trip yang dibuat. Silakan ke Tab 'Buat Trip'.");
    else:
        # Pilihan Trip
        trip = st.selectbox("Pilih Trip", st.session_state.trips, format_func=lambda t: t.title, key='select_trip_act')
        
        if not trip.destinations:
            st.warning(f"Trip '{trip.title}' belum punya destinasi. Tambahkan dulu di Tab 'Tambah Destinasi'.");
        else:
            # Pilihan Destinasi
            dest = st.selectbox("Pilih Destinasi", trip.destinations, format_func=lambda d: d.name, key='select_dest')

            st.markdown("---")
            with st.form("add_act"):
                c1, c2, c3 = st.columns([2, 1, 1])
                act_name = c1.text_input("Kegiatan / Aktivitas")
                biaya = c2.number_input("Biaya (Rp)", min_value=0, step=10000)
                durasi = c3.number_input("Durasi (Jam)", min_value=0.5, step=0.5)

                if st.form_submit_button("Simpan Aktivitas") and act_name:
                    dest.activities.append(Activity(act_name, biaya, durasi))
                    st.success(f"Aktivitas '{act_name}' berhasil ditambahkan ke {dest.name}!")


# --- TAB 4: LIHAT RANGKUMAN ---
with tab4:
    st.subheader("4. Rangkuman Semua Perjalanan")
    
    if not st.session_state.trips:
        st.info("Belum ada data perjalanan yang tercatat.")
    
    for trip in st.session_state.trips:
        # Menggunakan expander agar ringkas
        with st.expander(f"🗺 *{trip.title}* (Total Biaya: Rp {trip.total_cost():,.0f})"):
            st.caption(f"ID Trip: {trip.trip_id}")
            st.markdown("---")

            if not trip.destinations:
                st.write("Trip ini belum memiliki destinasi.")
            
            for d in trip.destinations:
                st.markdown(f"#### 📍 {d.name} ({d.location})")
                st.info(f"Biaya Destinasi: *Rp {d.total_cost():,.0f}*")

                if not d.activities:
                    st.write("• Belum ada aktivitas di destinasi ini")
                else:
                    for a in d.activities:
                        # Menampilkan detail aktivitas
                        st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• *{a.name}* | Rp {a.cost:,.0f} | {a.duration} jam")
                st.divider()


