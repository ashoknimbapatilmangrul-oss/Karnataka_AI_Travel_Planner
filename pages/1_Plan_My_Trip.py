import pandas as pd
import plotly.express as px
import streamlit as st

from utils.ai_helper import get_ai_tips
from utils.data_loader import load_destinations
from utils.exporter import itinerary_to_text
from utils.pdf_export import itinerary_to_pdf
from utils.planner import BUDGET_LEVELS, all_interests, estimate_cost, plan_trip
from utils.styles import card, hero, inject_css

st.set_page_config(page_title="Plan My Trip", page_icon="🗓️", layout="wide")
inject_css()

hero("🗓️ Plan My Trip", "Tell us what you love and we will build your Karnataka itinerary.")

destinations = load_destinations()
name_to_id = {d["name"]: d["id"] for d in destinations}

with st.form("trip_form"):
    c1, c2, c3 = st.columns(3)
    with c1:
        interests = st.multiselect(
            "Your interests", all_interests(), default=["Heritage", "Food"]
        )
    with c2:
        days = st.slider("Number of days", 1, 7, 3)
        travelers = st.number_input("Number of travellers", 1, 10, 2)
    with c3:
        budget_level = st.radio("Budget type", BUDGET_LEVELS, index=1, horizontal=True)
        choice = st.selectbox("Destination", ["Auto (best match)"] + list(name_to_id))
    submitted = st.form_submit_button("✨ Plan my trip", type="primary")

if submitted:
    if not interests:
        st.warning("Please select at least one interest.")
    else:
        dest_id = None if choice.startswith("Auto") else name_to_id[choice]
        result = plan_trip(interests, days, budget_level, travelers, dest_id)
        st.session_state["trip"] = {
            "result": result,
            "days": days,
            "budget": budget_level,
            "interests": interests,
        }

trip = st.session_state.get("trip")

if trip:
    result = trip["result"]
    dest = result["destination"]
    cost = result["cost"]

    st.header("📍 " + dest["name"])
    st.write(dest["description"])
    st.caption(
        result["travel_note"]
        + " Best months: " + dest["best_months"]
        + ". Must try: " + dest["famous_food"] + "."
    )
    if result["matched_interests"]:
        st.success("Matches your interests: " + ", ".join(result["matched_interests"]))

    tab1, tab2, tab3, tab4 = st.tabs(["🗓️ Itinerary", "💰 Cost", "🗺️ Map", "✨ Other options"])

    with tab1:
        for day in result["itinerary"]:
            items = ""
            for a in day["activities"]:
                hours = " <i>(" + str(a["hours"]) + " hrs)</i>" if a["hours"] else ""
                items += "<li><b>" + a["time"] + "</b>: " + a["name"] + hours + "</li>"
            note = '<p class="note">' + day["note"] + "</p>" if day["note"] else ""
            html = (
                '<div class="day-card"><h4>' + day["title"] + "</h4>"
                + note + "<ul>" + items + "</ul></div>"
            )
            st.markdown(html, unsafe_allow_html=True)

        st.subheader("🤖 Travel tips")
        if st.button("Get travel tips for this trip"):
            with st.spinner("Preparing your tips..."):
                text, source = get_ai_tips(trip)
            trip["ai_text"] = text
            trip["ai_source"] = source

        if trip.get("ai_text"):
            st.info(trip["ai_text"])
            st.caption("Tips source: " + trip.get("ai_source", "Built-in"))

        d1, d2 = st.columns(2)
        with d1:
            st.download_button(
                "📥 Download itinerary (TXT)",
                data=itinerary_to_text(trip),
                file_name="karnataka_itinerary.txt",
                mime="text/plain",
            )
        with d2:
            st.download_button(
                "📄 Download itinerary (PDF)",
                data=itinerary_to_pdf(trip),
                file_name="karnataka_itinerary.pdf",
                mime="application/pdf",
            )

    with tab2:
        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("Stay and food", format(cost["stay_food"], ","))
        m2.metric("Travel (round trip)", format(cost["travel"], ","))
        m3.metric("Tickets and local", format(cost["local"], ","))
        m4.metric("Per person", format(cost["per_person"], ","))
        m5.metric("Total (" + str(cost["travelers"]) + " people)", format(cost["group_total"], ","))
        st.caption("All amounts in Rs. These are approximate estimates per person.")

        left, right = st.columns(2)
        with left:
            pie = px.pie(
                names=["Stay and food", "Travel", "Tickets and local"],
                values=[cost["stay_food"], cost["travel"], cost["local"]],
                title="Where your money goes",
                color_discrete_sequence=["#1F6B4A", "#C9A227", "#8FBF9F"],
            )
            st.plotly_chart(pie)
        with right:
            compare = pd.DataFrame(
                {
                    "Budget type": BUDGET_LEVELS,
                    "Per person (Rs)": [
                        estimate_cost(dest, trip["days"], 1, b)["per_person"]
                        for b in BUDGET_LEVELS
                    ],
                }
            )
            bar = px.bar(
                compare,
                x="Budget type",
                y="Per person (Rs)",
                title="Same trip, different budgets",
                color_discrete_sequence=["#1F6B4A"],
            )
            st.plotly_chart(bar)

    with tab3:
        points = [{"lat": 12.9716, "lon": 77.5946}, {"lat": dest["lat"], "lon": dest["lon"]}]
        for alt in result["alternatives"]:
            points.append({"lat": alt["destination"]["lat"], "lon": alt["destination"]["lon"]})
        st.map(pd.DataFrame(points))
        st.caption("Map shows Bengaluru, your destination and the other suggested places.")

    with tab4:
        cols = st.columns(3)
        for col, alt in zip(cols, result["alternatives"]):
            d = alt["destination"]
            with col:
                card(
                    d["name"],
                    d["description"],
                    chips=d["tags"][:3],
                    gold_chips=["About Rs " + format(alt["cost"], ",") + " per person"],
                )
else:
    st.info("Form bharo aur **Plan my trip** dabao.")