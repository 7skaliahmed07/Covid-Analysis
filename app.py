import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import os
import requests
import json

db_path = 'covid.db'

# Function to build DB if missing
def build_db():
    st.info("First time setup: Fetching data and building database. This takes 30-60 seconds...")
    
    # Extract
    url = "https://disease.sh/v3/covid-19/historical?lastdays=all"
    response = requests.get(url)
    if response.status_code != 200:
        st.error("Could not fetch data from API")
        return False
    data = response.json()
    
    rows = []
    for country_data in data:
        country = country_data['country']
        timeline = country_data['timeline']
        cases = timeline['cases']
        deaths = timeline['deaths']
        recovered = timeline.get('recovered', {})
        for date, case_count in cases.items():
            row = {
                'country': country,
                'date': date,
                'cases': case_count,
                'deaths': deaths.get(date, 0),
                'recovered': recovered.get(date, 0)
            }
            rows.append(row)
    
    df = pd.DataFrame(rows)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(['country', 'date'])
    
    # Transform
    df['new_cases'] = df.groupby('country')['cases'].diff().fillna(0)
    df['new_deaths'] = df.groupby('country')['deaths'].diff().fillna(0)
    df['new_recovered'] = df.groupby('country')['recovered'].diff().fillna(0)
    df['growth_rate_pct'] = df['new_cases'] / df.groupby('country')['cases'].shift(1)
    df['growth_rate_pct'] = df['growth_rate_pct'].replace([float('inf'), -float('inf')], 0).fillna(0) * 100
    df['new_cases_7day'] = df.groupby('country')['new_cases'].transform(lambda x: x.rolling(7, min_periods=1).mean())
    df['new_deaths_7day'] = df.groupby('country')['new_deaths'].transform(lambda x: x.rolling(7, min_periods=1).mean())
    df['growth_rate_pct'] = df['growth_rate_pct'].round(2)
    df['new_cases_7day'] = df['new_cases_7day'].round(0)
    df['new_deaths_7day'] = df['new_deaths_7day'].round(0)
    df = df.fillna(0)
    
    # Load into SQLite
    conn_build = sqlite3.connect(db_path)
    df.to_sql('covid_data', conn_build, if_exists='replace', index=False)
    conn_build.close()
    
    st.success("Database built and ready!")
    return True

# Build if needed
if not os.path.exists(db_path):
    build_db()

# Cached connection
@st.cache_resource
def get_connection():
    return sqlite3.connect(db_path, check_same_thread=False)

conn = get_connection()

st.title("COVID-19 Global Dashboard")
st.markdown("Historical data up to March 2023 | ETL pipeline with SQLite")

# Sidebar
st.sidebar.header("Filters")
countries = pd.read_sql("SELECT DISTINCT country FROM covid_data ORDER BY country", conn)['country'].tolist()
selected_country = st.sidebar.selectbox("Select Country", countries, index=countries.index('USA') if 'USA' in countries else 0)

dates = pd.read_sql("SELECT DISTINCT date FROM covid_data ORDER BY date", conn)
all_dates = pd.to_datetime(dates['date'])
min_date = all_dates.min().date()
max_date = all_dates.max().date()

start_date, end_date = st.sidebar.date_input(
    "Date Range",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date)
)

# Queries with fresh conn reads
query = f"""
SELECT date, new_cases_7day, growth_rate_pct 
FROM covid_data 
WHERE country = '{selected_country}' 
AND date BETWEEN '{start_date}' AND '{end_date}'
"""
df_country = pd.read_sql(query, conn)
df_country['date'] = pd.to_datetime(df_country['date'])

global_query = f"""
SELECT date, SUM(cases) as total_cases 
FROM covid_data 
WHERE date BETWEEN '{start_date}' AND '{end_date}'
GROUP BY date
"""
df_global = pd.read_sql(global_query, conn)
df_global['date'] = pd.to_datetime(df_global['date'])

top10 = pd.read_sql("""
SELECT country, MAX(date) as latest_date, cases as total_cases
FROM covid_data
GROUP BY country
ORDER BY total_cases DESC
LIMIT 10
""", conn)

# Charts
col1, col2 = st.columns(2)

with col1:
    st.subheader(f"7-Day New Cases - {selected_country}")
    fig_cases = px.line(df_country, x='date', y='new_cases_7day')
    fig_cases.update_layout(height=400)
    st.plotly_chart(fig_cases, use_container_width=True)

with col2:
    st.subheader(f"Growth Rate % - {selected_country}")
    fig_growth = px.line(df_country, x='date', y='growth_rate_pct')
    fig_growth.update_layout(height=400)
    st.plotly_chart(fig_growth, use_container_width=True)

st.subheader("Global Total Cases")
fig_global = px.area(df_global, x='date', y='total_cases')
st.plotly_chart(fig_global, use_container_width=True)

st.subheader("Top 10 Countries by Total Cases")
st.dataframe(top10.style.format({"total_cases": "{:,}"}))

st.caption("Data source: disease.sh | Built with Python, pandas, SQLite, Streamlit")