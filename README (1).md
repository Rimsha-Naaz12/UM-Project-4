# SkyCity Auckland Restaurants & Bars — Channel Analytics

## Contents
- `app.py` — Streamlit dashboard
- `data/skycity_auckland_restaurants_bars.csv` — supplied dataset
- `research_paper.docx` — EDA, methodology, findings and recommendations
- `executive_summary.pdf` — stakeholder-facing summary
- `requirements.txt` — Python dependencies

## Run locally
```bash
cd skycity_auckland_project
pip install -r requirements.txt
streamlit run app.py
```

## Analytical note
The dataset contains one restaurant-level snapshot plus a `GrowthFactor`, not dated observations. Therefore the dashboard uses `MonthlyOrders * GrowthFactor` as a one-month scenario projection rather than claiming a statistically trained time-series forecast.

## Risk definitions
- Combined aggregator dependence = (Uber Eats orders + DoorDash orders) / MonthlyOrders.
- Aggregator-heavy = combined dependence >= 70%.
- Single-aggregator 70% test = max(Uber Eats share, DoorDash share) >= 70%.
- Channel Diversification Score = normalized Shannon entropy across the four order channels, scaled 0–100.
