import re
import time
from pathlib import Path

import requests

API = "https://commons.wikimedia.org/w/api.php"
HEADERS = {
    "User-Agent": "KarnatakaTravelPlanner/1.0 (student hackathon project; contact: your-email@example.com)"
}
OUT = Path("assets") / "images"
OUT.mkdir(parents=True, exist_ok=True)

# Search words for each destination (script tries them one by one)
SEARCHES = {
    "bengaluru": ["Vidhana Soudha Bengaluru", "Bangalore Palace", "Lalbagh Bangalore"],
    "mysuru": ["Mysore Palace", "Mysore Palace illuminated", "Mysuru Palace"],
    "coorg": ["Abbey Falls Coorg", "Coorg coffee plantation", "Madikeri Coorg landscape"],
    "hampi": ["Vittala Temple Hampi stone chariot", "Hampi ruins", "Virupaksha Temple Hampi"],
    "gokarna": ["Om Beach Gokarna", "Kudle Beach Gokarna", "Gokarna beach"],
    "chikkamagaluru": ["Mullayanagiri", "Chikmagalur hills", "Chikkamagaluru landscape"],
    "badami": ["Badami cave temples", "Badami Agastya lake", "Badami Karnataka"],
    "jogfalls": ["Jog Falls", "Jog Falls monsoon", "Gerusoppa Jog Falls Karnataka"],
    "udupi": ["Udupi Sri Krishna Temple", "Malpe beach Udupi", "St Mary's Island Udupi"],
    "belur": ["Chennakeshava Temple Belur", "Hoysaleswara Temple Halebidu", "Halebidu temple"],
}

BAD_WORDS = [
    "map", "logo", "flag", "seal", "emblem", "diagram", "plan", "locator",
    "icon", "coat of arms", "stamp", "poster", "painting", "drawing", "sketch",
    "inscription", "ruins of", "night", "interior", "statue of",
]


def clean_html(text):
    return re.sub(r"<[^>]+>", "", text or "").strip()


def search_photo(query):
    """Find a good landscape JPEG on Wikimedia Commons."""
    params = {
        "action": "query",
        "format": "json",
        "generator": "search",
        "gsrsearch": query + " filetype:bitmap",
        "gsrnamespace": 6,
        "gsrlimit": 15,
        "prop": "imageinfo",
        "iiprop": "url|mime|size|extmetadata",
        "iiurlwidth": 800,
    }
    r = requests.get(API, params=params, headers=HEADERS, timeout=30)
    r.raise_for_status()
    pages = r.json().get("query", {}).get("pages", {})
    ordered = sorted(pages.values(), key=lambda p: p.get("index", 999))

    for page in ordered:
        title = page.get("title", "")
        low = title.lower()
        if any(word in low for word in BAD_WORDS):
            continue
        info = (page.get("imageinfo") or [None])[0]
        if not info or info.get("mime") != "image/jpeg":
            continue
        if info.get("width", 0) < 1200 or info.get("width", 0) <= info.get("height", 0):
            continue
        meta = info.get("extmetadata", {})
        return {
            "title": title,
            "url": info.get("thumburl") or info.get("url"),
            "page": info.get("descriptionurl", ""),
            "artist": clean_html(meta.get("Artist", {}).get("value", "Unknown")),
            "license": meta.get("LicenseShortName", {}).get("value", "Free licence"),
        }
    return None


def download(url, path):
    for attempt in range(3):
        r = requests.get(url, headers=HEADERS, timeout=60)
        if r.status_code == 429:
            time.sleep(5 * (attempt + 1))
            continue
        r.raise_for_status()
        if len(r.content) < 20000:
            return False
        path.write_bytes(r.content)
        return True
    return False


credits = ["# Photo credits", "", "All photos are from Wikimedia Commons.", ""]

for dest_id, queries in SEARCHES.items():
    target = OUT / (dest_id + ".jpg")
    if target.exists():
        print("SKIP (already there):", target.name)
        continue

    done = False
    for q in queries:
        try:
            found = search_photo(q)
            time.sleep(1.5)
            if found and download(found["url"], target):
                size_kb = round(target.stat().st_size / 1024)
                print("OK  ", target.name, "-", size_kb, "KB -", found["title"])
                credits.append(
                    "- **" + dest_id + ".jpg**: " + found["title"].replace("File:", "")
                    + " by " + found["artist"] + " (" + found["license"] + "). "
                    + found["page"]
                )
                done = True
                break
        except Exception as e:
            print("   error for", q, "->", e)
            time.sleep(2)

    if not done:
        print("NOT FOUND:", dest_id, "(emoji banner will be used)")

credits_file = OUT / "CREDITS.md"
old = credits_file.read_text(encoding="utf-8").splitlines() if credits_file.exists() else []
new_lines = [c for c in credits[4:] if c not in old]
if new_lines:
    header = [] if old else credits[:4]
    credits_file.write_text("\n".join(old + header + new_lines) + "\n", encoding="utf-8")

print("\nFinished. Check the assets/images folder and CREDITS.md")