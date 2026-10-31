import os

import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://api.anthropic.com/v1/messages"
MODEL = os.getenv("ANTHROPIC_MODEL", "claude-haiku-5-5")


def _get_key():
    """Read the API key from .env, or from Streamlit secrets after deployment."""
    key = os.getenv("ANTHROPIC_API_KEY")
    if key and key != "your_api_key_here":
        return key
    try:
        import streamlit as st

        return st.secrets.get("ANTHROPIC_API_KEY")
    except Exception:
        return None


def fallback_tips(trip):
    """Built-in tips. Works without internet or API key."""
    dest = trip["result"]["destination"]
    interests = set(trip["interests"])
    lines = []
    lines.append("Best time to visit " + dest["name"] + ": " + dest["best_months"] + ".")
    lines.append("Must try food: " + dest["famous_food"] + ".")

    packing = ["water bottle", "sunscreen", "power bank", "comfortable walking shoes"]
    if "Beach" in interests:
        packing.append("swimwear and flip-flops")
    if "Adventure" in interests or "Nature" in interests:
        packing.append("light rain jacket and a small first-aid kit")
    if "Spiritual" in interests or "Heritage" in interests:
        packing.append("modest clothes for temples and a cloth bag for shoes")
    lines.append("Pack: " + ", ".join(packing) + ".")

    km = dest["from_bengaluru_km"]
    if km > 300:
        lines.append(
            "Long journey ("
            + str(km)
            + " km): book an overnight bus or train early, or take a cab for comfort."
        )
    elif km > 0:
        lines.append("Start early in the morning to avoid traffic on the way from Bengaluru.")

    lines.append("Local tip: carry some cash, as small shops and villages may not accept UPI.")
    lines.append("Learn one Kannada line: Namaskara (Hello) and Dhanyavadagalu (Thank you).")
    return "\n".join(lines)


def get_ai_tips(trip):
    """Return (text, source). source is 'AI' or 'Built-in'."""
    key = _get_key()
    if not key:
        return fallback_tips(trip), "Built-in"

    result = trip["result"]
    dest = result["destination"]
    plan = ""
    for day in result["itinerary"]:
        names = ", ".join(a["name"] for a in day["activities"])
        plan += day["title"] + " -> " + names + "\n"

    prompt = (
        "You are a friendly Karnataka travel guide.\n"
        "Trip: " + dest["name"] + ", " + str(trip["days"]) + " days, "
        + trip["budget"] + " budget, "
        + str(result["cost"]["travelers"]) + " travellers.\n"
        "Interests: " + ", ".join(trip["interests"]) + ".\n"
        "Plan:\n" + plan + "\n"
        "Write 120 to 150 words: one warm welcome line, 3 practical local tips, "
        "what to pack, and one useful Kannada phrase with its meaning. "
        "Use plain text only. No markdown symbols, no emojis, English letters only."
    )

    try:
        response = requests.post(
            API_URL,
            headers={
                "x-api-key": key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": MODEL,
                "max_tokens": 600,
                "messages": [{"role": "user", "content": prompt}],
            },
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
        text = "".join(b.get("text", "") for b in data.get("content", []))
        if text.strip():
            return text.strip(), "AI"
    except Exception:
        pass

    return fallback_tips(trip), "Built-in"