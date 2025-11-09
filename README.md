# COVID-19 Data Analysis ETL Pipeline

A simple ETL pipeline to pull COVID-19 data from public APIs, clean it, calculate trends, store in SQLite, and visualize with interactive dashboards.

## Features
- Extract: Fetches historical COVID data using Python requests
- Transform: Cleans data and calculates daily growth rates with pandas
- Load: Saves to a local SQLite database
- Visualize: Interactive plots with Plotly and dashboards in Jupyter or Streamlit

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