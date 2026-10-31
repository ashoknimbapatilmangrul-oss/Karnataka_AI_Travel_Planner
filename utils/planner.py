from utils.data_loader import load_destinations

BUDGET_LEVELS = ["budget", "standard", "luxury"]

# Approx round-trip travel rate per person per km (bus / train / cab share)
TRAVEL_RATE_PER_KM = {"budget": 1.5, "standard": 3, "luxury": 7}

MAX_HOURS_PER_DAY = 6
MAX_PLACES_PER_DAY = 3
TIME_SLOTS = ["Morning (9:00 AM)", "Afternoon (1:00 PM)", "Evening (4:30 PM)"]


def all_interests():
    """Return a sorted list of every interest tag in the data."""
    tags = set()
    for d in load_destinations():
        tags.update(d["tags"])
        for p in d["places"]:
            tags.update(p["tags"])
    return sorted(tags)


def score_destination(dest, interests):
    """Higher score = better match with the traveller's interests."""
    interests = set(interests)
    score = len(set(dest["tags"]) & interests) * 2
    for p in dest["places"]:
        score += len(set(p["tags"]) & interests)
    return score


def estimate_cost(dest, days, travelers, budget_level):
    """Simple cost estimate (all numbers in Rs)."""
    stay_food = dest["daily_cost"][budget_level] * days
    travel = int(dest["from_bengaluru_km"] * 2 * TRAVEL_RATE_PER_KM[budget_level])
    local = int(stay_food * 0.10)  # entry tickets, local transport, small extras
    per_person = stay_food + travel + local
    return {
        "stay_food": stay_food,
        "travel": travel,
        "local": local,
        "per_person": per_person,
        "group_total": per_person * travelers,
        "travelers": travelers,
    }


def recommend_destinations(interests, budget_level, days, top_n=3):
    """Rank all destinations by interest match, then by lower cost."""
    results = []
    for d in load_destinations():
        score = score_destination(d, interests)
        # Short trip: far places lose points because travel eats the time
        if days <= 2 and d["from_bengaluru_hours"] > 6:
            score -= 3
        cost = estimate_cost(d, days, 1, budget_level)["per_person"]
        results.append({"destination": d, "score": score, "cost": cost})
    results.sort(key=lambda r: (-r["score"], r["cost"]))
    return results[:top_n]


def build_itinerary(dest, interests, days):
    """Create a day-by-day plan for one destination."""
    interests = set(interests)
    # Best-matching places first (sort is stable, so equal places keep order)
    remaining = sorted(
        dest["places"], key=lambda p: -len(set(p["tags"]) & interests)
    )

    itinerary = []
    for day_no in range(1, days + 1):
        todays = []
        hours = 0
        for place in remaining[:]:
            if len(todays) >= MAX_PLACES_PER_DAY:
                break
            if not todays or hours + place["hours"] <= MAX_HOURS_PER_DAY:
                todays.append(place)
                hours += place["hours"]
                remaining.remove(place)

        if todays:
            activities = [
                {
                    "time": TIME_SLOTS[i],
                    "name": p["name"],
                    "hours": p["hours"],
                    "tags": p["tags"],
                }
                for i, p in enumerate(todays)
            ]
            title = f"Day {day_no}: {todays[0]['name']}"
            if len(todays) > 1:
                title += " and more"
        else:
            title = f"Day {day_no}: Relax, local food and shopping"
            activities = [
                {
                    "time": TIME_SLOTS[0],
                    "name": f"Slow morning, try local food: {dest['famous_food']}",
                    "hours": 0,
                    "tags": ["Food"],
                },
                {
                    "time": TIME_SLOTS[1],
                    "name": "Local market walk and souvenir shopping",
                    "hours": 0,
                    "tags": ["Culture"],
                },
                {
                    "time": TIME_SLOTS[2],
                    "name": "Sunset time and rest at your stay",
                    "hours": 0,
                    "tags": ["Relaxation"],
                },
            ]

        note = ""
        if day_no == 1 and dest["from_bengaluru_km"] > 0:
            note = "Start early from Bengaluru, plan the first activity after you reach and check in."
        if day_no == days and dest["from_bengaluru_km"] > 0:
            note = (note + " " if note else "") + "Check out and begin the return journey by evening."

        itinerary.append({"day": day_no, "title": title, "note": note, "activities": activities})

    return itinerary


def plan_trip(interests, days, budget_level, travelers, destination_id=None):
    """Main function used by the website."""
    ranked = recommend_destinations(interests, budget_level, days, top_n=100)

    if destination_id:
        chosen = next(r for r in ranked if r["destination"]["id"] == destination_id)
    else:
        chosen = ranked[0]

    dest = chosen["destination"]
    alternatives = [r for r in ranked if r["destination"]["id"] != dest["id"]][:3]

    all_tags = set(dest["tags"])
    for p in dest["places"]:
        all_tags.update(p["tags"])
    matched = sorted(all_tags & set(interests))

    km = dest["from_bengaluru_km"]
    if km == 0:
        travel_note = "No long travel needed, you are already in Bengaluru."
    else:
        travel_note = f"About {km} km from Bengaluru ({dest['from_bengaluru_hours']} hours by road)."

    return {
        "destination": dest,
        "matched_interests": matched,
        "travel_note": travel_note,
        "itinerary": build_itinerary(dest, interests, days),
        "cost": estimate_cost(dest, days, travelers, budget_level),
        "alternatives": alternatives,
    }