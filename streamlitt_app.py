import streamlit as st

# ============================================
#                 OOP CLASSES
# ============================================

class Activity:
    def __init__(self, name, cost, duration):
        self.name = name
        self.cost = cost
        self.duration = duration

    def __str__(self):
        return f"{self.name} - Rp{self.cost} ({self.duration} jam)"


class Destination:
    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.activities = []

    def add_activity(self, activity):
        self.activities.append(activity)

    def total_cost(self):
        return sum(a.cost for a in self.activities)

    def __str__(self):
        return f"{self.name} - {self.location}"


class Trip:
    def __init__(self, trip_id, title):
        self.trip_id = trip_id
        self.title = title
        self.destinations = []

    def add_destination(self, destination):
        self.destinations.append(destination)

    def total_trip_cost(self):
        return sum(d.total_cost() for d in self.destinations)


class User:
    def __init__(self, name):
        self.name = name
        self.trips = []

    def add_trip(self, trip):
        self.trips.append(trip)


# ============================================
#          STREAMLIT STATE MANAGEMENT
# ============================================

if "user" not in st.session_state:
    st.session_state.user = User("User")


user = st.session_state.user

st.title("🌍 Trip Planner Sederhana (Streamlit + OOP)")


# ============================================
#            MENU NAVIGASI
# ============================================
menu = st.sidebar.radio(
    "Pilih Menu",
    ["Buat Trip", "Tambah Destinasi", "Tambah Aktivitas", "Lihat Trip"]
)

# ============================================
#              BUAT TRIP BARU
# ============================================
if menu == "Buat Trip":
    st.header("➕ Buat Trip Baru")

    with st.form("form_trip"):
        trip_id = st.text_input("ID Trip")
        title = st.text_input("Judul Trip")
        submit = st.form_submit_button("Buat Trip")

        if submit:
            if trip_id and title:
                new_trip = Trip(trip_id, title)
                user.add_trip(new_trip)
                st.success("Trip berhasil dibuat!")
            else:
                st.warning("Isi semua form dulu!")


# ============================================
#         TAMBAH DESTINASI KE TRIP
# ============================================
elif menu == "Tambah Destinasi":
    st.header("🏝 Tambah Destinasi ke Trip")

    if not user.trips:
        st.warning("Belum ada trip. Buat dulu di menu 'Buat Trip'.")
    else:
        trip_selected = st.selectbox(
            "Pilih Trip",
            user.trips,
            format_func=lambda t: f"{t.trip_id} - {t.title}"
        )

        with st.form("form_destinasi"):
            name = st.text_input("Nama Destinasi")
            loc = st.text_input("Lokasi")
            submit = st.form_submit_button("Tambah Destinasi")

            if submit:
                d = Destination(name, loc)
                trip_selected.add_destination(d)
                st.success("Destinasi ditambahkan!")


# ============================================
#         TAMBAH AKTIVITAS KE DESTINASI
# ============================================
elif menu == "Tambah Aktivitas":
    st.header("🎯 Tambah Aktivitas ke Destinasi")

    if not user.trips:
        st.warning("Belum ada trip.")
    else:
        trip_selected = st.selectbox(
            "Pilih Trip",
            user.trips,
            format_func=lambda t: f"{t.trip_id} - {t.title}"
        )

        if not trip_selected.destinations:
            st.warning("Trip ini belum punya destinasi.")
        else:
            dest_selected = st.selectbox(
                "Pilih Destinasi",
                trip_selected.destinations,
                format_func=lambda d: f"{d.name} - {d.location}"
            )

            with st.form("form_aktivitas"):
                name = st.text_input("Nama Aktivitas")
                cost = st.number_input("Biaya", min_value=0)
                duration = st.number_input("Durasi (jam)", min_value=0.0)
                submit = st.form_submit_button("Tambah Aktivitas")

                if submit:
                    act = Activity(name, cost, duration)
                    dest_selected.add_activity(act)
                    st.success("Aktivitas berhasil ditambahkan!")


# ============================================
#               LIHAT SEMUA TRIP
# ============================================
elif menu == "Lihat Trip":
    st.header("📋 Daftar Trip")

    if not user.trips:
        st.warning("Belum ada trip.")
    else:
        for t in user.trips:
            st.subheader(f"🧳 {t.title}")

            if not t.destinations:
                st.write("Belum ada destinasi.")
            else:
                for d in t.destinations:
                    st.write(f"**{d.name}** – {d.location}")

                    if not d.activities:
                        st.write("• Belum ada aktivitas")
                    else:
                        for a in d.activities:
                            st.write(f"• {a}")

            st.info(f"Total biaya trip: **Rp{t.total_trip_cost()}**")


