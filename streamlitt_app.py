# =======================================================
#        TRIP PLANNER SANGAT SEDERHANA (OOP DASAR)
# =======================================================

# -----------------------
# CLASS ACTIVITY
# -----------------------
class Activity:
    def __init__(self, name, cost, duration):
        self.name = name
        self.cost = cost
        self.duration = duration

    def __str__(self):
        return f"{self.name} - Rp{self.cost} ({self.duration} jam)"


# -----------------------
# CLASS DESTINATION
# -----------------------
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


# -----------------------
# CLASS TRIP
# -----------------------
class Trip:
    def __init__(self, trip_id, title):
        self.trip_id = trip_id
        self.title = title
        self.destinations = []

    def add_destination(self, destination):
        self.destinations.append(destination)

    def total_trip_cost(self):
        return sum(d.total_cost() for d in self.destinations)

    def __str__(self):
        return f"Trip {self.trip_id}: {self.title}"


# -----------------------
# CLASS USER
# -----------------------
class User:
    def __init__(self, name):
        self.name = name
        self.trips = []

    def add_trip(self, trip):
        self.trips.append(trip)


# ==========================================================
#                 PROGRAM UTAMA (MENU)
# ==========================================================

user = User("User")  # buat user default

def menu():
    print("\n===== TRIP PLANNER SEDERHANA =====")
    print("1. Buat Trip Baru")
    print("2. Tambah Destinasi ke Trip")
    print("3. Tambah Aktivitas ke Destinasi")
    print("4. Lihat Semua Trip")
    print("5. Keluar")
    return input("Pilih menu: ")

def buat_trip():
    trip_id = input("Masukkan ID Trip: ")
    title = input("Masukkan judul trip: ")
    trip = Trip(trip_id, title)
    user.add_trip(trip)
    print("Trip berhasil dibuat!\n")

def pilih_trip():
    if not user.trips:
        print("Belum ada trip.")
        return None
    print("\nDaftar Trip:")
    for t in user.trips:
        print(f"{t.trip_id}. {t.title}")
    trip_id = input("Pilih ID Trip: ")
    for t in user.trips:
        if t.trip_id == trip_id:
            return t
    print("Trip tidak ditemukan.")
    return None

def tambah_destinasi():
    trip = pilih_trip()
    if trip:
        name = input("Nama destinasi: ")
        loc = input("Lokasi: ")
        d = Destination(name, loc)
        trip.add_destination(d)
        print("Destinasi ditambahkan!\n")

def tambah_aktivitas():
    trip = pilih_trip()
    if not trip:
        return
    
    if not trip.destinations:
        print("Trip belum punya destinasi.")
        return
    
    print("\nDaftar Destinasi:")
    for i, d in enumerate(trip.destinations):
        print(f"{i+1}. {d.name}")

    idx = int(input("Pilih destinasi (nomor): ")) - 1
    if idx < 0 or idx >= len(trip.destinations):
        print("Pilihan tidak valid.")
        return

    dest = trip.destinations[idx]

    name = input("Nama aktivitas: ")
    cost = int(input("Biaya: "))
    duration = float(input("Durasi (jam): "))

    act = Activity(name, cost, duration)
    dest.add_activity(act)
    print("Aktivitas ditambahkan!\n")

def lihat_trip():
    if not user.trips:
        print("Belum ada trip.")
        return
    
    for t in user.trips:
        print(f"\n=== {t.title} ===")
        
        if not t.destinations:
            print("  (Belum ada destinasi)")
        else:
            for d in t.destinations:
                print(f"- {d.name} ({d.location})")
                
                if not d.activities:
                    print("   * Belum ada aktivitas")
                else:
                    for a in d.activities:
                        print(f"   * {a}")

        print(f"Total biaya trip: Rp{t.total_trip_cost()}")
    print()

# ==========================================================
#                   MAIN LOOP
# ==========================================================
while True:
    pilihan = menu()

    if pilihan == "1":
        buat_trip()
    elif pilihan == "2":
        tambah_destinasi()
    elif pilihan == "3":
        tambah_aktivitas()
    elif pilihan == "4":
        lihat_trip()
    elif pilihan == "5":
        print("Terima kasih! Program selesai.")
        break
    else:
        print("Pilihan tidak valid.")

