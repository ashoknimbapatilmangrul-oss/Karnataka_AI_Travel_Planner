import streamlit as st

from utils.data_loader import load_destinations
from utils.styles import (
    card,
    dest_card,
    footer,
    hero,
    inject_css,
    section_title,
    stats,
)

st.set_page_config(page_title="Karnataka AI Travel Planner", page_icon="🧭", layout="wide")
inject_css()

hero(
    "Discover Karnataka, Your Way",
    "Tell us your interests, days and budget. Our AI travel planner builds a personalised "
    "Karnataka itinerary with cost, map and Kannada phrases in seconds.",
    badge="🌿 Kannada Technology Challenge",
)

b1, b2, b3 = st.columns([1, 1, 2])
with b1:
    st.page_link("pages/1_Plan_My_Trip.py", label="Plan My Trip", icon="🧭")
with b2:
    st.page_link("pages/2_Explore_Destinations.py", label="Explore Places", icon="🌄")

destinations = load_destinations()
total_places = sum(len(d["places"]) for d in destinations)

stats(
    [
        (len(destinations), "Destinations"),
        (total_places, "Places to visit"),
        (3, "Budget types"),
        (15, "Kannada phrases"),
    ]
)

section_title("How it works", "Three simple steps to your perfect trip")
s1, s2, s3 = st.columns(3)
with s1:
    card("1. Tell us what you love", "Pick interests like Heritage, Beach, Food, Nature or Adventure.", gold_chips=["Step 1"])
with s2:
    card("2. Set time and budget", "Choose number of days, budget type and number of travellers.", gold_chips=["Step 2"])
with s3:
    card("3. Get your plan", "Receive a day-by-day itinerary, cost estimate, map, tips and a PDF.", gold_chips=["Step 3"])

section_title("Popular destinations", "Handpicked places across coast, hills and heritage")
featured_ids = ["coorg", "hampi", "mysuru", "gokarna", "udupi", "jogfalls"]
featured = [d for d in destinations if d["id"] in featured_ids]
for i in range(0, len(featured), 3):
    cols = st.columns(3)
    for col, d in zip(cols, featured[i:i + 3]):
        with col:
            dest_card(d)

section_title("Why choose this planner", "Built for travellers, powered by smart logic and AI")
w1, w2, w3 = st.columns(3)
with w1:
    card("🎯 Personalised", "Every plan changes with your interests, days, budget and group size.")
with w2:
    card("💰 Clear costs", "See stay, food, travel and local costs with simple charts before you go.")
with w3:
    card("🗣️ Kannada ready", "Learn useful Kannada phrases so you can connect with locals.")

footer()