def itinerary_to_text(trip):
    """Turn a saved trip (dictionary) into a plain text itinerary."""
    result = trip["result"]
    dest = result["destination"]
    cost = result["cost"]

    lines = []
    lines.append("KARNATAKA AI TRAVEL PLANNER")
    lines.append("=" * 40)
    lines.append("Destination : " + dest["name"])
    lines.append("Days        : " + str(trip["days"]))
    lines.append("Budget type : " + trip["budget"])
    lines.append("Travellers  : " + str(cost["travelers"]))
    lines.append("Interests   : " + ", ".join(trip["interests"]))
    lines.append("Best months : " + dest["best_months"])
    lines.append("Must try    : " + dest["famous_food"])
    lines.append(result["travel_note"])
    lines.append("")

    for day in result["itinerary"]:
        lines.append(day["title"])
        if day["note"]:
            lines.append("  Note: " + day["note"])
        for a in day["activities"]:
            hours = " (" + str(a["hours"]) + " hrs)" if a["hours"] else ""
            lines.append("  - " + a["time"] + ": " + a["name"] + hours)
        lines.append("")

    lines.append("ESTIMATED COST (Rs)")
    lines.append("  Stay and food : " + format(cost["stay_food"], ","))
    lines.append("  Travel        : " + format(cost["travel"], ","))
    lines.append("  Tickets/local : " + format(cost["local"], ","))
    lines.append("  Per person    : " + format(cost["per_person"], ","))
    lines.append("  Group total   : " + format(cost["group_total"], ","))
    lines.append("")
    lines.append("Prices are approximate and may change. Happy travels!")
    return "\n".join(lines)