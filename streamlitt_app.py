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
        self.is_completed = False  # Status trip: False (Aktif), True (Selesai/History)

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
    
    # Ambil trip yang masih aktif
    def get_active_trips(self):
        return [t for t in self.trips if not t.is_completed]

    # Ambil trip yang sudah selesai (history)
    def get_history_trips(self):
        return [t for t in self.trips if t.is_completed]


# ============================================
#           STREAMLIT STATE MANAGEMENT
# ============================================

if "user" not in st.session_state:
    # Inisialisasi User baru jika belum ada di session
    st.session_state.user = User("Pengguna")

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
        trip_id = st.text_input("ID Trip (Unik, misal: T01)")
        title = st.text_input("Judul Trip (misal: Liburan Bali)")
        submit = st.form_submit_button("Buat Trip")

        if submit:
            if trip_id and title:
                # Cek apakah ID sudah dipakai
                if any(t.trip_id == trip_id for t in user.trips):
                    st.error("ID Trip sudah digunakan, ganti yang lain.")
                else:
                    new_trip = Trip(trip_id, title)
                    user.add_trip(new_trip)
                    st.success(f"Trip '{title}' berhasil dibuat!")
            else:
                st.warning("Mohon isi ID dan Judul Trip.")


# ============================================
#          TAMBAH DESTINASI KE TRIP
# ============================================
elif menu == "Tambah Destinasi":
    st.header("🏝 Tambah Destinasi")
    active_trips = user.get_active_trips()

    if not active_trips:
        st.warning("Tidak ada trip aktif. Silakan buat trip dulu.")
    else:
        trip_selected = st.selectbox(
            "Pilih Trip Aktif",
            active_trips,
            format_func=lambda t: f"{t.trip_id} - {t.title}"
        )

        with st.form("form_destinasi"):
            name = st.text_input("Nama Destinasi (misal: Pantai Kuta)")
            loc = st.text_input("Lokasi (misal: Badung)")
            submit = st.form_submit_button("Tambah Destinasi")

            if submit:
                if name and loc:
                    d = Destination(name, loc)
                    trip_selected.add_destination(d)
                    st.success(f"Destinasi '{name}' berhasil ditambahkan!")
                else:
                    st.warning("Nama dan Lokasi harus diisi.")


# ============================================
#         TAMBAH AKTIVITAS KE DESTINASI
# ============================================
elif menu == "Tambah Aktivitas":
    st.header("🎯 Tambah Aktivitas")
    active_trips = user.get_active_trips()

    if not active_trips:
        st.warning("Tidak ada trip aktif.")
    else:
        trip_selected = st.selectbox(
            "Pilih Trip",
            active_trips,
            format_func=lambda t: f"{t.trip_id} - {t.title}"
        )

        if not trip_selected.destinations:
            st.warning("Trip ini belum punya destinasi. Tambah destinasi dulu.")
        else:
            dest_selected = st.selectbox(
                "Pilih Destinasi",
                trip_selected.destinations,
                format_func=lambda d: f"{d.name} - {d.location}"
            )

            with st.form("form_aktivitas"):
                name = st.text_input("Nama Aktivitas (misal: Surfing)")
                cost = st.number_input("Biaya (Rp)", min_value=0, step=1000)
                duration = st.number_input("Durasi (jam)", min_value=0.0, step=0.5)
                submit = st.form_submit_button("Tambah Aktivitas")

                if submit:
                    if name:
                        act = Activity(name, cost, duration)
                        dest_selected.add_activity(act)
                        st.success("Aktivitas berhasil disimpan!")
                    else:
                        st.warning("Nama aktivitas wajib diisi.")


# ============================================
#           LIHAT TRIP AKTIF
# ============================================
elif menu == "Lihat Trip Aktif":
    st.header("🛫 Trip Sedang Berjalan")
    active_trips = user.get_active_trips()

    if not active_trips:
        st.info("Tidak ada trip yang sedang aktif.")
    else:
        for t in active_trips:
            with st.expander(f"🧳 {t.title} (ID: {t.trip_id})", expanded=True):
                st.write(f"*Total Biaya Estimasi: Rp{t.total_trip_cost():,}*")
                
                if not t.destinations:
                    st.caption("Belum ada destinasi.")
                else:
                    for d in t.destinations:
                        st.markdown(f"📍 {d.name}** ({d.location}) - Rp{d.total_cost():,}")
                        for a in d.activities:
                            st.text(f"   • {a}")
                
                st.divider()
                # Tombol Selesai
                col1, col2 = st.columns([3, 1])
                with col2:
                    if st.button(f"✅ Selesai Trip", key=f"finish_{t.trip_id}"):
                        t.mark_as_completed()
                        st.rerun()


# ============================================
#           RIWAYAT TRIP (HISTORY)
# ============================================
elif menu == "Riwayat Trip":
    st.header("📜 Riwayat Perjalanan (History)")
    history_trips = user.get_history_trips()

    if not history_trips:
        st.info("Belum ada trip yang selesai.")
    else:
        # Tabel Ringkasan
        data_summary = []
        for t in history_trips:
            data_summary.append({
                "ID Trip": t.trip_id,
                "Judul": t.title,
                "Destinasi": len(t.destinations),
                "Total Biaya": f"Rp{t.total_trip_cost():,}"
            })
        
        st.table(data_summary)

        st.markdown("---")
        st.markdown("### 🔎 Detail Riwayat")
        for t in history_trips:
            with st.expander(f"✅ {t.title}"):
                for d in t.destinations:
                    st.write(f"📍 {d.name} ({d.location})")
                    for a in d.activities:
                        st.caption(f"   - {a}")
