import base64
from pathlib import Path

import streamlit as st

IMAGE_DIR = Path(__file__).resolve().parent.parent / "assets" / "images"

# emoji, gradient start, gradient end for each destination (used if no photo)
THEMES = {
    "bengaluru": ("🏙️", "#1F6B4A", "#3FA66B"),
    "mysuru": ("🏰", "#8B5E00", "#D4A017"),
    "coorg": ("☕", "#14532D", "#4C9A5F"),
    "hampi": ("🛕", "#8A3B12", "#D9822B"),
    "gokarna": ("🏖️", "#0B6E8A", "#38B6C9"),
    "chikkamagaluru": ("⛰️", "#2F5D3A", "#7DB36B"),
    "badami": ("🗿", "#7A4A1E", "#C98B4B"),
    "jogfalls": ("💦", "#0E5A7A", "#4FB0D6"),
    "udupi": ("🍛", "#B4531A", "#E8A33D"),
    "belur": ("🏛️", "#5B3A29", "#B08968"),
}
DEFAULT_THEME = ("📍", "#1F6B4A", "#3FA66B")

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Poppins:wght@400;500;600&display=swap');

html, body, [class*="css"], .stMarkdown, p, li, label {
    font-family: 'Poppins', sans-serif;
}
h1, h2, h3, h4 {
    font-family: 'Playfair Display', serif !important;
    color: #14532D;
}
.block-container {padding-top: 2rem; max-width: 1200px;}
footer {visibility: hidden;}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #14532D 0%, #1F6B4A 100%);
}
[data-testid="stSidebar"] * {color: #F3E9C6 !important;}
[data-testid="stSidebarNav"] a {
    border-radius: 10px;
    margin: 2px 6px;
}
[data-testid="stSidebarNav"] a:hover {background: rgba(255, 255, 255, 0.15);}

/* Hero */
.hero {
    position: relative;
    overflow: hidden;
    background: linear-gradient(135deg, #0F3D22 0%, #1F6B4A 55%, #2E8B57 100%);
    padding: 2.6rem 2.2rem;
    border-radius: 22px;
    border-bottom: 6px solid #C9A227;
    margin-bottom: 1.6rem;
    box-shadow: 0 10px 30px rgba(20, 83, 45, 0.25);
}
.hero::before {
    content: "";
    position: absolute;
    right: -60px; top: -60px;
    width: 260px; height: 260px;
    border-radius: 50%;
    background: rgba(201, 162, 39, 0.18);
}
.hero::after {
    content: "";
    position: absolute;
    right: 120px; bottom: -90px;
    width: 200px; height: 200px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.08);
}
.hero h1 {
    color: #FFFFFF !important;
    margin: 0;
    font-size: 2.6rem;
    position: relative;
    z-index: 1;
}
.hero p {
    color: #F3E9C6 !important;
    margin: 0.6rem 0 0 0;
    font-size: 1.1rem;
    max-width: 720px;
    position: relative;
    z-index: 1;
}
.badge {
    display: inline-block;
    background: #C9A227;
    color: #1E2A24;
    font-size: 0.8rem;
    font-weight: 600;
    padding: 4px 14px;
    border-radius: 999px;
    margin-bottom: 0.8rem;
    position: relative;
    z-index: 1;
}

/* Stats */
.stats {display: flex; gap: 1rem; margin-bottom: 1.5rem; flex-wrap: wrap;}
.stat {
    flex: 1;
    min-width: 160px;
    background: #FFFFFF;
    border: 1px solid #E6DCC0;
    border-radius: 16px;
    padding: 1rem 1.2rem;
    text-align: center;
    box-shadow: 0 3px 12px rgba(0, 0, 0, 0.06);
}
.stat .num {
    font-family: 'Playfair Display', serif;
    font-size: 2.2rem;
    font-weight: 700;
    color: #1F6B4A;
    line-height: 1.1;
}
.stat .lbl {color: #7A5B00; font-size: 0.9rem; font-weight: 500;}

/* Section title */
.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.8rem;
    color: #14532D;
    margin: 1.8rem 0 0.2rem 0;
}
.section-title::after {
    content: "";
    display: block;
    width: 60px; height: 4px;
    background: #C9A227;
    border-radius: 4px;
    margin-top: 6px;
}
.section-sub {color: #5B6B62; margin-bottom: 1rem;}

/* Cards */
.card {
    background: #FFFFFF;
    border: 1px solid #E6DCC0;
    border-left: 5px solid #C9A227;
    border-radius: 16px;
    padding: 1.1rem 1.2rem;
    margin-bottom: 1rem;
    box-shadow: 0 3px 12px rgba(0, 0, 0, 0.06);
    min-height: 190px;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.card:hover {transform: translateY(-5px); box-shadow: 0 12px 26px rgba(0, 0, 0, 0.13);}
.card h4 {color: #14532D; margin: 0 0 0.4rem 0; font-size: 1.15rem;}
.card p {color: #3B3B3B; margin: 0 0 0.6rem 0; font-size: 0.93rem;}

/* Destination card */
.dcard {
    background: #FFFFFF;
    border: 1px solid #E6DCC0;
    border-radius: 18px;
    overflow: hidden;
    margin-bottom: 0.8rem;
    box-shadow: 0 3px 12px rgba(0, 0, 0, 0.07);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.dcard:hover {transform: translateY(-6px); box-shadow: 0 14px 28px rgba(0, 0, 0, 0.16);}
.dbanner {
    height: 120px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 3.4rem;
}
.dbody {padding: 1rem 1.1rem 0.9rem 1.1rem;}
.dbody h4 {margin: 0 0 0.3rem 0; color: #14532D; font-size: 1.15rem;}
.dbody p {color: #3B3B3B; font-size: 0.9rem; margin: 0 0 0.5rem 0;}
.dmeta {color: #7A5B00; font-size: 0.82rem; font-weight: 500; margin-top: 0.3rem;}

/* Chips */
.chip {
    display: inline-block;
    background: #E8F3EC;
    color: #14532D;
    border-radius: 999px;
    padding: 2px 11px;
    margin: 2px 4px 2px 0;
    font-size: 0.78rem;
    font-weight: 500;
}
.chip-gold {background: #FBF1CC; color: #7A5B00;}

/* Itinerary day */
.day-card {
    background: #FFFFFF;
    border: 1px solid #E6DCC0;
    border-top: 5px solid #1F6B4A;
    border-radius: 14px;
    padding: 1rem 1.3rem;
    margin-bottom: 1rem;
    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
}
.day-card h4 {color: #14532D; margin: 0 0 0.3rem 0;}
.day-card ul {margin: 0.3rem 0 0 0; color: #3B3B3B;}
.note {color: #7A5B00; font-size: 0.88rem; margin: 0 0 0.3rem 0;}

/* Buttons */
.stButton > button, [data-testid="stFormSubmitButton"] button,
.stDownloadButton > button, [data-testid="stPageLink"] a {
    background: linear-gradient(135deg, #1F6B4A, #2E8B57);
    color: #FFFFFF !important;
    border: none;
    border-radius: 12px;
    padding: 0.55rem 1.2rem;
    font-weight: 600;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}
.stButton > button:hover, [data-testid="stFormSubmitButton"] button:hover,
.stDownloadButton > button:hover, [data-testid="stPageLink"] a:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(31, 107, 74, 0.35);
    color: #FFFFFF !important;
}

/* Metrics and tabs */
[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid #E6DCC0;
    border-radius: 14px;
    padding: 0.8rem 1rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}
[data-testid="stMetricValue"] {color: #1F6B4A;}
.stTabs [data-baseweb="tab"] {font-weight: 600; font-size: 1rem;}
.stTabs [aria-selected="true"] {color: #1F6B4A;}

/* Footer */
.site-footer {
    margin-top: 2.5rem;
    background: linear-gradient(135deg, #0F3D22, #1F6B4A);
    border-top: 5px solid #C9A227;
    color: #F3E9C6;
    text-align: center;
    padding: 1.4rem 1rem;
    border-radius: 18px;
    font-size: 0.92rem;
}
.site-footer b {color: #FFFFFF;}
"""


@st.cache_data(show_spinner=False)
def _photo_uri(dest_id):
    """Return the destination photo as a data URI, or None if no photo exists."""
    for ext in ("jpg", "jpeg", "png", "webp"):
        path = IMAGE_DIR / (dest_id + "." + ext)
        if path.exists():
            mime = "jpeg" if ext in ("jpg", "jpeg") else ext
            data = base64.b64encode(path.read_bytes()).decode()
            return "data:image/" + mime + ";base64," + data
    return None


def inject_css():
    st.markdown("<style>" + CSS + "</style>", unsafe_allow_html=True)


def hero(title, subtitle, badge=None):
    badge_html = '<span class="badge">' + badge + "</span><br>" if badge else ""
    html = (
        '<div class="hero">' + badge_html
        + "<h1>" + title + "</h1><p>" + subtitle + "</p></div>"
    )
    st.markdown(html, unsafe_allow_html=True)


def stats(items):
    """items = list of (number, label)."""
    boxes = ""
    for num, label in items:
        boxes += (
            '<div class="stat"><div class="num">' + str(num)
            + '</div><div class="lbl">' + label + "</div></div>"
        )
    st.markdown('<div class="stats">' + boxes + "</div>", unsafe_allow_html=True)


def section_title(title, sub=None):
    html = '<div class="section-title">' + title + "</div>"
    if sub:
        html += '<div class="section-sub">' + sub + "</div>"
    st.markdown(html, unsafe_allow_html=True)


def card(title, body, chips=None, gold_chips=None):
    chip_html = ""
    for c in chips or []:
        chip_html += '<span class="chip">' + c + "</span>"
    for c in gold_chips or []:
        chip_html += '<span class="chip chip-gold">' + c + "</span>"
    html = (
        '<div class="card"><h4>' + title + "</h4><p>" + body + "</p>"
        + chip_html + "</div>"
    )
    st.markdown(html, unsafe_allow_html=True)


def dest_card(d):
    """Destination card: real photo if available, else colourful emoji banner."""
    emoji, c1, c2 = THEMES.get(d["id"], DEFAULT_THEME)
    photo = _photo_uri(d["id"])

    if photo:
        banner = (
            '<div class="dbanner" style="height:170px;'
            "background-image: linear-gradient(180deg, rgba(0,0,0,0) 55%, rgba(0,0,0,0.35) 100%), url("
            + photo
            + ');background-size:cover;background-position:center;"></div>'
        )
    else:
        banner = (
            '<div class="dbanner" style="background: linear-gradient(135deg, '
            + c1 + ", " + c2 + ');">' + emoji + "</div>"
        )

    chip_html = ""
    for t in d["tags"][:4]:
        chip_html += '<span class="chip">' + t + "</span>"
    km = "In the city" if d["from_bengaluru_km"] == 0 else str(d["from_bengaluru_km"]) + " km from Bengaluru"

    html = (
        '<div class="dcard">' + banner
        + '<div class="dbody"><h4>' + d["name"] + "</h4>"
        "<p>" + d["description"] + "</p>" + chip_html
        + '<div class="dmeta">📅 ' + d["best_months"] + " &nbsp;|&nbsp; 🚗 " + km
        + " &nbsp;|&nbsp; Rs " + format(d["daily_cost"]["standard"], ",") + "/day</div>"
        "</div></div>"
    )
    st.markdown(html, unsafe_allow_html=True)


def footer():
    html = (
        '<div class="site-footer"><b>🧭 Karnataka AI Travel Planner</b><br>'
        "Discover Karnataka, Your Way. | Kannada Technology Challenge | Problem Statement 06<br>"
        "ಕರ್ನಾಟಕಕ್ಕೆ ಸ್ವಾಗತ</div>"
    )
    st.markdown(html, unsafe_allow_html=True)