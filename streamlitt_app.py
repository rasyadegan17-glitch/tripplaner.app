import streamlit as st
from dataclasses import dataclass, field
from typing import List

# ============================================
#             MODEL DATA (SAMA)
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
#             INIT STATE
# ============================================
st.set_page_config(layout="wide") # Pakai mode layar lebar
if "trips" not in st.session_state:
    st.session_state.trips = []

# ============================================
#             TAMPILAN UTAMA
# ============================================
st.title("🚀 One-Page Trip Planner")

# Bagi layar jadi 2 kolom: Kiri (Input) - Kanan (Hasil)
col_input, col_view = st.columns([1, 1.5]) 

# --------------------------------------------
# KOLOM KIRI: FORM INPUT (Pakai Tabs)
# --------------------------------------------
with col_input:
    st.subheader("📝 Input Data")
    # Tabs supaya rapi dan tidak panjang ke bawah
    tab1, tab2, tab3 = st.tabs(["1. Buat Trip", "2. + Destinasi", "
