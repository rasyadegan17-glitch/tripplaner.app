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
        return sum(a.cost for a in self.activities)

@dataclass
class Trip:
    trip_id: str
    title: str
    destinations: List[Destination] = field(default_factory=list)

    def total_cost(self):
        return sum(d.total_cost() for d in self.destinations)

# ============================================
#             MAIN APP LOGIC
# ============================================

# 1. State Management (Simpan data di memori)
if "trips" not in st.session_state:
    st.session_state.trips = []

st.title("✈️ Trip Planner Sat-Set")

# 2. Sidebar Menu
menu = st.sidebar.radio("Menu", ["Buat Trip", "Tambah Destinasi", "Tambah Aktivitas", "Lihat Trip"])

# --------------------------------------------
# FITUR 1: BUAT TRIP
# --------------------------------------------
if menu == "Buat Trip":
    st.subheader("Buat Trip Baru")
    with st.form("new_trip"):
        c1, c2 = st.columns(2)
        tid = c1.text_input("ID Unik")
        ttl = c2.text_input("Nama Trip")
        if st.form_submit_button("Simpan") and tid and ttl:
            st.session_state.trips.append(Trip(tid, ttl))
            st.success(f"Trip '{ttl}' berhasil dibuat!")

# --------------------------------------------
# FITUR 2: TAMBAH DESTINASI
# --------------------------------------------
elif menu == "Tambah Destinasi":
    st.subheader("Tambah Destinasi")
    
    if not st.session_state.trips:
        st.warning("Buat Trip dulu!"); st.stop()

    # Pilih Trip
    trip = st.selectbox("Pilih Trip", st.session_state.trips, format_func=lambda t: t.title)
    
    with st.form("add_dest"):
        c1, c2 = st.columns(2)
        name = c1.text_input("Nama Tempat")
        loc = c2.text_input("Lokasi / Kota")
        
        if st.form_submit_button("Tambah Destinasi") and name:
            trip.destinations.append(Destination(name, loc))
            st.success(f"{name} ditambahkan ke {trip.title}!")

# --------------------------------------------
# FITUR 3: TAMBAH AKTIVITAS
# --------------------------------------------
elif menu == "Tambah Aktivitas":
    st.subheader("Tambah Aktivitas")

    if not st.session_state.trips:
        st.warning("Buat Trip dulu!"); st.stop()

    # Logic: Pilih Trip -> Filter Destinasi -> Pilih Destinasi
    trip = st.selectbox("Pilih Trip", st.session_state.trips, format_func=lambda t: t.title)
    
    if not trip.destinations:
        st.warning("Trip ini belum punya destinasi!"); st.stop()

    dest = st.selectbox("Pilih Destinasi", trip.destinations, format_func=lambda d: d.name)

    with st.form("add_act"):
        c1, c2, c3 = st.columns([2, 1, 1])
        act_name = c1.text_input("Kegiatan")
        biaya = c2.number_input("Biaya (Rp)", min_value=0, step=5000)
        durasi = c3.number_input("Durasi (Jam)", min_value=0.5)

        if st.form_submit_button("Simpan Aktivitas") and act_name:
            dest.activities.append(Activity(act_name, biaya, durasi))
            st.success("Aktivitas tersimpan!")

# --------------------------------------------
# FITUR 4: LIHAT SUMMARY
# --------------------------------------------
elif menu == "Lihat Trip":
    st.subheader("Rangkuman Perjalanan")
    
    if not st.session_state.trips:
        st.info("Belum ada data perjalanan.")
    
    for trip in st.session_state.trips:
        # Pakai Expander biar rapi (bisa di-collapse)
        with st.expander(f"🗺️ {trip.title} (Total: Rp {trip.total_cost():,.0f})"):
            st.caption(f"ID: {trip.trip_id}")
            
            if not trip.destinations:
                st.write("*Belum ada destinasi*")
            
            for d in trip.destinations:
                st.markdown(f"**📍 {d.name}** ({d.location}) - *Rp {d.total_cost():,.0f}*")
                for a in d.activities:
                    st.text(f"   • {a.name}: Rp {a.cost:,.0f} ({a.duration} jam)")
                st.divider()
