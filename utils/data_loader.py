import json
from pathlib import Path

import pandas as pd

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "destinations.json"


def load_destinations():
    """Read destinations.json and return a list of dictionaries."""
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def destinations_dataframe():
    """Return a simple table (DataFrame) of all destinations."""
    rows = []
    for d in load_destinations():
        rows.append(
            {
                "Destination": d["name"],
                "Region": d["region"],
                "Best Months": d["best_months"],
                "Interests": ", ".join(d["tags"]),
                "Km from Bengaluru": d["from_bengaluru_km"],
                "Budget/day (Rs)": d["daily_cost"]["budget"],
                "Standard/day (Rs)": d["daily_cost"]["standard"],
                "Luxury/day (Rs)": d["daily_cost"]["luxury"],
            }
        )
    return pd.DataFrame(rows)