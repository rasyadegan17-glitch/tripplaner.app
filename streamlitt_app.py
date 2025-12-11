import streamlit as st

# ============================================
#                  OOP CLASSES
# ============================================

class Activity:
    # PERBAIKAN: Gunakan _init_ (double underscore)
    def _init_(self, name, cost, duration):
        self.name = name
        self.cost = cost
        self.duration = duration

    # PERBAIKAN: Gunakan _str_ (double underscore)
    def _str_(self):
        return f"{self.name} - Rp{self.cost} ({self.duration} jam)"


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

    def add_destination(self, destination):
        self.destinations.append(destination)

    def total_trip_cost(self):
        return sum(d.total_cost() for d in self.destinations)


class User:
    def _init_(self, name):
        self.name = name
        self.trips = []

    def add_trip(self, trip):
        self.trips.append(trip)


# ============================================
#           STREAMLIT STATE MANAGEMENT
# ============================================

if "user" not in st.session_state:
    st.session_state.user = User("User")

user = st.session_state.user

st.title("🌍 Trip Planner Sederhana (Streamlit + OOP)")


# ============================================
#             MENU NAVIGASI
# ============================================
menu = st.sidebar.radio(
    "Pilih Menu",
    ["Buat Trip", "Tambah Destinasi", "Tambah Aktivitas", "Lihat Trip"]
)

# ============================================
#               BUAT TRIP BARU
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
                st.success(f"Trip '{title}' berhasil dibuat!")
            else:
                st.warning("Isi semua form dulu!")


# ============================================
#          TAMBAH DESTINASI KE TRIP
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
                if name and loc:
                    d = Destination(name, loc)
                    trip_selected.add_destination(d)
                    st.success(f"Destinasi '{name}' ditambahkan!")
                else:
                    st.warning("Nama dan Lokasi harus diisi.")


# ============================================
#         TAMBAH AKTIVITAS KE DESTINASI
# ============================================
elif menu == "Tambah Aktivitas":
    st.header("🎯 Tambah Aktivitas ke Destinasi")

    if not user.trips:
        st.warning("Belum ada trip.")
    else:
        # Pilih Trip Dulu
        trip_selected = st.selectbox(
            "Pilih Trip",
            user.trips,
            format_func=lambda t: f"{t.trip_id} - {t.title}"
        )

        if not trip_selected.destinations:
            st.warning("Trip ini belum punya destinasi. Tambahkan destinasi dulu.")
        else:
            # Pilih Destinasi di dalam Trip tersebut
            dest_selected = st.selectbox(
                "Pilih Destinasi",
                trip_selected.destinations,
                format_func=lambda d: f"{d.name} - {d.location}"
            )

            with st.form("form_aktivitas"):
                name = st.text_input("Nama Aktivitas")
                cost = st.number_input("Biaya (Rp)", min_value=0, step=1000)
                duration = st.number_input("Durasi (jam)", min_value=0.0, step=0.5)
                submit = st.form_submit_button("Tambah Aktivitas")

                if submit:
                    if name:
                        act = Activity(name, cost, duration)
                        dest_selected.add_activity(act)
                        st.success(f"Aktivitas '{name}' berhasil ditambahkan!")
                    else:
                        st.warning("Nama aktivitas harus diisi.")


# ============================================
#                LIHAT SEMUA TRIP
# ============================================
elif menu == "Lihat Trip":
    st.header("📋 Daftar Trip")

    if not user.trips:
        st.warning("Belum ada trip.")
    else:
        for t in user.trips:
            st.markdown("---")
            st.subheader(f"🧳 {t.title} (ID: {t.trip_id})")
            
            total_biaya = t.total_trip_cost()

            if not t.destinations:
                st.caption("Belum ada destinasi.")
            else:
                for d in t.destinations:
                    st.markdown(f"📍 {d.name}** ({d.location})")
                    st.markdown(f"&nbsp;&nbsp;&nbsp;Biaya Destinasi: Rp{d.total_cost()}")

                    if not d.activities:
                        st.write("&nbsp;&nbsp;&nbsp;• Belum ada aktivitas")
                    else:
                        for a in d.activities:
                            st.write(f"&nbsp;&nbsp;&nbsp;• {a}") # Ini memanggil _str_ Activity

            st.info(f"💰 *Total Biaya Trip: Rp{total_biaya:,}*")
