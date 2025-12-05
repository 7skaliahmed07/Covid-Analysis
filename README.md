# COVID-19 Data Analysis ETL Pipeline
![image_alt](https://github.com/7skaliahmed07/Covid-Analysis/blob/3c07061f075c26ff467aa04d1f397983e5bdb39c/overview.png)

This project automates the full flow of collecting, cleaning, storing and exploring COVID-19 case data. It retrieves updated data from public APIs, prepares it with pandas, loads it into SQLite and presents trends through static plots and an interactive Streamlit dashboard. The layout is structured so you can maintain or extend the pipeline easily.

## Repository Structure
.
├── README.md
├── requirements.txt
│
├── data/
│   ├── raw/
│   │   └── covid_raw.csv
│   ├── clean/
│   │   └── covid_clean.csv
│   └── covid.db
│
├── etl/
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   ├── check_countries.py
│   └── visualize.py
│
├── app/
│   └── app.py
│
├── plots/
│   ├── overview.png
│   ├── global_cases.png
│   ├── new_cases_usa.png
│   └── growth_rate_usa.png
│
├── notebooks/
│   ├── exploration.ipynb
│   └── validation.ipynb
│
├── utils/
│   ├── db.py
│   ├── helpers.py
│   └── logging_config.py
│
└── tests/
    ├── test_extract.py
    ├── test_transform.py
    └── test_load.py


## Features

Extract
Fetches global COVID-19 time-series data from public API sources.

Transform
Cleans raw inputs, handles missing values, converts date fields and calculates daily changes and growth rates.

Load
Stores processed tables in a local SQLite database.

Visualize
Creates time-series plots and supports interactive exploration through a Streamlit dashboard.

The project is designed for learning and experimentation with lightweight tools.

Built for learning purposes on macOS with free tools only.

## How to Run
1. Clone the repo
2. Create virtual env: `python3 -m venv venv && source venv/bin/activate`
3. Install deps: `pip install -r requirements.txt`
4. Run the pipeline: `python etl_pipeline.py` (or open notebooks)
5. View dashboard: `streamlit run app.py`

Data source: Reliable public COVID APIs (updated in code).

Feel free to fork and improve!


## Live Dashboard

Check out the interactive dashboard here: 
[Live App] [COVID-19 Data Analysis ETL Pipeline](https://covid-analysis-uzair.streamlit.app/)

It pulls fresh data on first load, then runs instantly. Pick any country, zoom the charts, slide the dates – all the ETL happens behind the scenes.
