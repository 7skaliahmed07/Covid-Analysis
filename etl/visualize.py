import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
from app import get_connection

# Connect to DB
conn = get_connection()

# Load data for a country (let's do USA first)
country = 'USA'
df = pd.read_sql(f"SELECT date, new_cases_7day, growth_rate_pct FROM covid_data WHERE country = '{country}'", conn)
df['date'] = pd.to_datetime(df['date'])

# Plot 1: 7-day new cases
plt.figure(figsize=(12, 6))
plt.plot(df['date'], df['new_cases_7day'])
plt.title(f'7-Day Average New Cases in {country}')
plt.ylabel('New Cases')
plt.xlabel('Date')
plt.grid(True)
plt.savefig('new_cases_usa.png')
print("Saved new_cases_usa.png")

# Plot 2: Growth rate
plt.figure(figsize=(12, 6))
plt.plot(df['date'], df['growth_rate_pct'])
plt.title(f'Daily Growth Rate % in {country}')
plt.ylabel('Growth Rate %')
plt.xlabel('Date')
plt.grid(True)
plt.savefig('growth_rate_usa.png')
print("Saved growth_rate_usa.png")

# Bonus: World total cases over time
world = pd.read_sql("SELECT date, SUM(cases) as total_cases FROM covid_data GROUP BY date", conn)
world['date'] = pd.to_datetime(world['date'])
plt.figure(figsize=(12, 6))
plt.plot(world['date'], world['total_cases'])
plt.title('Global Total Cases')
plt.ylabel('Total Cases')
plt.xlabel('Date')
plt.grid(True)
plt.savefig('global_cases.png')
print("Saved global_cases.png")

conn.close()
print("All plots done! Openparallel the PNG files.")