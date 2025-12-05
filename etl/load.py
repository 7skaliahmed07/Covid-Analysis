import pandas as pd
import sqlite3
from app import get_connection

print("Loading clean data...")
df = pd.read_csv("covid_clean.csv")

# Create (or connect to) the database
conn = get_connection()

# Load the DataFrame into SQLite (creates table if not exists)
df.to_sql("covid_data", conn, if_exists="replace", index=False)

conn.close()

print("Load complete! Data is now in covid.db")
print("Table name: covid_data")
print("Total rows loaded:", len(df))

# Quick test query: top 10 countries by latest total cases
conn = get_connection()
query = """
SELECT country, MAX(date) as latest_date, cases as total_cases
FROM covid_data
GROUP BY country
ORDER BY total_cases DESC
LIMIT 10
"""
top10 = pd.read_sql(query, conn)
print("\nTop 10 countries by total cases:")
print(top10)
conn.close()
