import streamlit as st

from utils.styles import card, hero, inject_css

st.set_page_config(page_title="About", page_icon="ℹ️", layout="wide")
inject_css()

hero("ℹ️ About This Project", "Problem Statement 06: AI Travel Planner for Karnataka")

st.write(
    "Planning a Karnataka trip is confusing: too many places, scattered information and "
    "unclear budgets. This app creates a personalised itinerary from the traveller's "
    "interests, available time, budget and preferred type of experience."
)

a, b, c = st.columns(3)
with a:
    card("Personalised", "Itinerary changes with interests, days, budget and group size.")
with b:
    card("Transparent cost", "Clear estimate for stay, food, travel and local expenses.")
with c:
    card("Works offline from AI", "Smart rule-based planner always works, AI only makes it better.")

st.subheader("Tech stack")
st.write("Python, Streamlit, Pandas, Plotly, JSON data, GitHub, Streamlit Community Cloud.")

st.subheader("Future scope")
st.write(
    "- Live weather and festival calendar\n"
    "- Hotel and transport booking links\n"
    "- Kannada voice assistant\n"
    "- Offline mobile app"
)