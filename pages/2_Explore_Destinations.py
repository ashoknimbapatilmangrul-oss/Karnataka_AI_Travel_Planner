import pandas as pd
import plotly.express as px
import streamlit as st

from utils.data_loader import load_destinations
from utils.planner import all_interests
from utils.styles import dest_card, footer, hero, inject_css, section_title

st.set_page_config(page_title="Explore Destinations", page_icon="🌄", layout="wide")
inject_css()

hero(
    "Explore Destinations",
    "Browse the best places in Karnataka, from golden beaches to Hoysala temples.",
    badge="🌄 10 handpicked destinations",
)

destinations = load_destinations()
regions = ["All regions"] + sorted({d["region"] for d in destinations})

f1, f2 = st.columns(2)
with f1:
    chosen_tags = st.multiselect("Filter by interest (leave empty to see all)", all_interests())
with f2:
    chosen_region = st.selectbox("Region", regions)


def matches(d):
    if chosen_region != "All regions" and d["region"] != chosen_region:
        return False
    if not chosen_tags:
        return True
    tags = set(d["tags"])
    for p in d["places"]:
        tags.update(p["tags"])
    return bool(tags & set(chosen_tags))


filtered = [d for d in destinations if matches(d)]
st.write("Showing **" + str(len(filtered)) + "** destinations")

if not filtered:
    st.warning("No destination matches this filter. Try removing one.")
else:
    for i in range(0, len(filtered), 3):
        cols = st.columns(3)
        for col, d in zip(cols, filtered[i:i + 3]):
            with col:
                dest_card(d)
                with st.expander("Places to visit"):
                    for p in d["places"]:
                        st.write("- " + p["name"] + " (" + str(p["hours"]) + " hrs)")

    section_title("Map", "Where these destinations are in Karnataka")
    st.map(pd.DataFrame([{"lat": d["lat"], "lon": d["lon"]} for d in filtered]))

    section_title("Cost comparison", "Standard budget cost per day (Rs)")
    chart_df = pd.DataFrame(
        {
            "Destination": [d["name"] for d in filtered],
            "Cost per day (Rs)": [d["daily_cost"]["standard"] for d in filtered],
        }
    )
    fig = px.bar(
        chart_df,
        x="Destination",
        y="Cost per day (Rs)",
        color="Cost per day (Rs)",
        color_continuous_scale=["#8FBF9F", "#1F6B4A", "#C9A227"],
    )
    st.plotly_chart(fig)

footer()