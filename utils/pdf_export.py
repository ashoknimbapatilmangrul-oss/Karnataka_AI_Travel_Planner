from fpdf import FPDF


def _clean(text):
    """The built-in PDF font supports only basic Latin letters, so clean the text."""
    swaps = {
        "\u2019": "'",
        "\u2018": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2013": "-",
        "\u2014": "-",
        "\u2022": "-",
        "\u20b9": "Rs ",
    }
    for old, new in swaps.items():
        text = text.replace(old, new)
    return text.encode("latin-1", "replace").decode("latin-1")


def _line(pdf, text, size=11, style="", color=(30, 42, 36)):
    pdf.set_font("Helvetica", style, size)
    pdf.set_text_color(*color)
    pdf.multi_cell(0, 6, _clean(text), new_x="LMARGIN", new_y="NEXT")


def itinerary_to_pdf(trip):
    """Create a PDF and return it as bytes."""
    result = trip["result"]
    dest = result["destination"]
    cost = result["cost"]

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Green title bar
    pdf.set_fill_color(20, 83, 45)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 14, "Karnataka AI Travel Planner", new_x="LMARGIN", new_y="NEXT", align="C", fill=True)
    pdf.ln(4)

    _line(pdf, dest["name"], 16, "B", (20, 83, 45))
    _line(
        pdf,
        str(trip["days"]) + " days | " + trip["budget"].title() + " budget | "
        + str(cost["travelers"]) + " travellers",
    )
    _line(pdf, "Interests: " + ", ".join(trip["interests"]))
    _line(pdf, "Best months: " + dest["best_months"] + " | Must try: " + dest["famous_food"])
    _line(pdf, result["travel_note"])
    pdf.ln(3)

    for day in result["itinerary"]:
        _line(pdf, day["title"], 13, "B", (20, 83, 45))
        if day["note"]:
            _line(pdf, "Note: " + day["note"], 10, "I", (122, 91, 0))
        for a in day["activities"]:
            hours = " (" + str(a["hours"]) + " hrs)" if a["hours"] else ""
            _line(pdf, "- " + a["time"] + ": " + a["name"] + hours)
        pdf.ln(2)

    _line(pdf, "Estimated cost (Rs)", 13, "B", (20, 83, 45))
    _line(pdf, "Stay and food: " + format(cost["stay_food"], ","))
    _line(pdf, "Travel (round trip): " + format(cost["travel"], ","))
    _line(pdf, "Tickets and local: " + format(cost["local"], ","))
    _line(pdf, "Per person: " + format(cost["per_person"], ","), 11, "B")
    _line(pdf, "Group total: " + format(cost["group_total"], ","), 11, "B")
    pdf.ln(3)

    if trip.get("ai_text"):
        _line(pdf, "Travel tips", 13, "B", (20, 83, 45))
        _line(pdf, trip["ai_text"])
        pdf.ln(3)

    _line(pdf, "Prices are approximate and may change. Happy travels!", 9, "I", (110, 110, 110))
    return bytes(pdf.output())