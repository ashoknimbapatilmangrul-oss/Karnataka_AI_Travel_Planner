# 🧭 Karnataka AI Travel Planner

**Discover Karnataka, Your Way.**

Problem Statement 06: **AI Travel Planner for Karnataka** (Kannada Technology Challenge).

An AI-powered travel planner that creates personalised Karnataka itineraries based on a traveller's interests, available time, budget and preferred type of experience.

## Live Demo

- Deployed app: _add your Streamlit link here_
- Demo video: _add your video link here_

## Features

- Personalised day-by-day itinerary from interests, days, budget type and number of travellers
- Smart destination recommendation across 10 Karnataka destinations
- Cost estimate (stay, food, travel, local) with charts
- Map view of the destination and other suggestions
- AI travel tips (works with a built-in fallback if no API key is set)
- Itinerary download as TXT and PDF
- Explore page with filters by interest and region
- Kannada phrases for travellers (Kannada script plus pronunciation)

## Tech Stack

Python, Streamlit, Pandas, Plotly, FPDF2, Requests, python-dotenv, JSON data, GitHub, Streamlit Community Cloud.

## Project Structure

```
Karnataka_AI_Travel_Planner
├── app.py                  Home page
├── pages/                  Plan My Trip, Explore, About, Kannada Phrases
├── utils/                  Planner logic, AI helper, PDF/TXT export, styles
├── data/destinations.json  Destination data
├── assets/images/          Destination photos
├── .streamlit/config.toml  Theme
├── requirements.txt
└── .env.example
```

## Setup and Run

```bash
git clone https://github.com/ashoknimbapatilmangrul-oss/Karnataka_AI_Travel_Planner.git
cd Karnataka_AI_Travel_Planner
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

On Windows you can also use `py -m pip install -r requirements.txt` and `py -m streamlit run app.py`.

## Optional: AI tips

The app works without any API key (built-in tips are used). To enable AI tips, copy `.env.example` to `.env` and add your key:

```
ANTHROPIC_API_KEY=your_api_key_here
```

Never commit your `.env` file.

## How it works

1. The user selects interests, days, budget type and travellers.
2. Each destination is scored by how well its tags and places match the interests.
3. The best destination is chosen (or the user picks one).
4. Places are arranged into day-wise slots with realistic hours per day.
5. Cost is estimated from daily cost, travel distance and local expenses.
6. Optional AI adds local tips; otherwise built-in tips are shown.

## Future Scope

- Live weather and festival calendar
- Hotel and transport booking links
- Kannada voice assistant
- More destinations and offline mobile app

## Photo Credits

Destination photos are from free-licence sources. See `assets/images/CREDITS.md` for photographer names and links.