import streamlit as st

# ============================================
#                  OOP CLASSES
# ============================================

class Activity:
    def _init_(self, name, cost, duration):
        self.name = name
        self.cost = cost
        self.duration = duration

    def _str_(self):
        return f"{self.name} - Rp{self.cost:,} ({self.duration} jam)"


class Destination:
    def _init_(self, name, location):
        self.name = name
        self.location = location
        self.activities = []

    def add_activity(self, activity):
        self.activities.append(activity)

    def total_cost(self):
        return sum(a.cost for a in self.activities)

    def _str_(self):
        return f"{self.name} - {self.location}"


class Trip:
    def _init_(self, trip_id, title):
        self.trip_id = trip_id
        self.title = title
        self.destinations = []
        self.is_completed = False  # <--- FITUR BARU: Status trip

    def add_destination(self, destination):
        self.destinations.append(destination)

    def total_trip_cost(self):
        return sum(d.total_cost() for d in self.destinations)
    
    def mark_as_completed(self):
        self.is_completed = True


class User:
    def _init_(self, name):
        self.name = name
        self.trips = []

    def add_trip(self, trip):
        self.trips.append(trip)
    
    # Helper untuk mengambil trip aktif saja
    def get_active_trips(self):
        return [t for t in self.trips if not t.is_completed]

    # Helper untuk mengambil history trip saja
    def get_history_trips(self):
        return [t for t in self.trips if t.is_completed]


# ============================================
#           STREAMLIT STATE MANAGEMENT
# ============================================

if "user" not in st.session_state:
    st.session_state.user = User("User")

user = st.session_state.user

st.title("🌍 Trip Planner + History")


# ============================================
#             MENU NAVIGASI
# ============================================
menu = st.sidebar.radio(
    "Pilih Menu",
    ["Buat Trip", "Tambah Destinasi", "Tambah Aktivitas", "Lihat Trip Aktif", "Riwayat Trip"]
)

# ============================================
#               BUAT TRIP BARU
# ============================================
if menu == "Buat Trip":
    st.header("➕ Buat Trip Baru")
    with st.form("form_trip"):
        trip_id = st.text_input("ID Trip (Unik)")
        title = st.text_input("Judul Trip")
        submit = st.form_submit_button("Buat Trip")

        if submit:
            if trip_id and title:
                # Cek ID unik sederhana
                if any(t.trip_id == trip_id for t in user.trips):
                    st.error("ID Trip sudah digunakan, pakai ID lain.")
                else:
                    new_trip = Trip(trip_id, title)
                    user.add_trip(new_trip)
                    st.success(f"Trip '{title}' berhasil dibuat!")
            else:
                st.warning("Isi semua form dulu!")


# ============================================
#          TAMBAH DESTINASI KE TRIP
# ============================================
# ============================================
#          TAMBAH DESTINASI KE TRIP
# ============================================
elif menu == "Tambah Destinasi":
    st.header("🏝 Tambah Destinasi")
    active_trips = user.get_active_trips() # Hanya bisa tambah ke trip aktif

    if not active_trips:
        st.warning("Tidak ada trip aktif. Silakan buat trip baru.")
    else:
        # PERBAIKAN DI SINI: Pastikan st.selectbox tertutup sempurna
        trip_selected = st.selectbox(
            "Pilih Trip Aktif",
            active_trips,
            format_func=lambda t: f"{t.trip_id} - {t.title}"
        )

        with st.form("form_destinasi"):
            name = st.text_input("Nama Destinasi")
            loc = st.text_input("Lokasi")
            submit = st.form_submit_button("Tambah Destinasi")

            if submit:
                if name and loc:
                    d = Destination(name, loc)
                    trip_selected.add_destination(d)
                    st.success(f"Destinasi '{name}' ditambahkan ke {trip_selected.title}!")
                else:
                    st.warning("Isi data destinasi.")
