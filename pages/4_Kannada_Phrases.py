import streamlit as st

from utils.phrases import PHRASES, categories
from utils.styles import card, hero, inject_css

st.set_page_config(page_title="Kannada Phrases", page_icon="🗣️", layout="wide")
inject_css()

hero("🗣️ Kannada Phrases for Travellers", "Learn simple Kannada for travel, shopping, food and emergencies.")

f1, f2 = st.columns(2)
with f1:
    category = st.selectbox("Category", ["All"] + categories())
with f2:
    search = st.text_input("Search (English)", "")

shown = [
    p for p in PHRASES
    if (category == "All" or p["category"] == category)
    and search.lower() in p["english"].lower()
]

st.write("Showing **" + str(len(shown)) + "** phrases")

if not shown:
    st.warning("No phrase found. Try another word.")
else:
    for i in range(0, len(shown), 3):
        cols = st.columns(3)
        for col, p in zip(cols, shown[i:i + 3]):
            with col:
                body = (
                    '<span style="font-size:1.5rem;color:#14532D;">' + p["kannada"] + "</span>"
                    + "<br><i>Say: " + p["say"] + "</i>"
                )
                card(p["english"], body, gold_chips=[p["category"]])

st.caption("Tip: Locals love it when visitors try even one Kannada word. 😊")