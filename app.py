import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

st.title("COVID-19 Global Dashboard")
st.markdown("Historical data up to March 2023 | ETL pipeline with SQLite backend")

# Connect to DB
conn = sqlite3.connect('covid.db')

# Sidebar controls
st.sidebar.header("Filters")
countries = pd.read_sql("SELECT DISTINCT country FROM covid_data ORDER BY country", conn)['country'].tolist()
selected_country = st.sidebar.selectbox("Select Country", countries, index=countries.index('USA') if 'USA' in countries else 0)

# Date range picker (fixed version)
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

# Load data for selected country and date range
query = f"""
SELECT date, new_cases_7day, growth_rate_pct 
FROM covid_data 
WHERE country = '{selected_country}' 
AND date BETWEEN '{start_date}' AND '{end_date}'
"""
df_country = pd.read_sql(query, conn)
df_country['date'] = pd.to_datetime(df_country['date'])

# Global data
global_query = f"""
SELECT date, SUM(cases) as total_cases 
FROM covid_data 
WHERE date BETWEEN '{start_date}' AND '{end_date}'
GROUP BY date
"""
df_global = pd.read_sql(global_query, conn)
df_global['date'] = pd.to_datetime(df_global['date'])

# Top 10 latest
top10 = pd.read_sql("""
SELECT country, MAX(date) as latest_date, cases as total_cases
FROM covid_data
GROUP BY country
ORDER BY total_cases DESC
LIMIT 10
""", conn)

conn.close()

# Layout
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