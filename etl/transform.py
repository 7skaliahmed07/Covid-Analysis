import pandas as pd

print("loading raw data....")

df = pd.read_csv("./covid_raw.csv")

df['date'] = pd.to_datetime(df["date"])

# Sort
df = df.sort_values(['country','date'])

print("Calculating daily new cases and deaths...")


# Daily new cases = difference from previous day
df['new_cases'] = df.groupby("country")['cases'].diff().fillna(0)

# Daily new deaths
df['new_deaths'] = df.groupby("country")['deaths'].diff().fillna(0)

# Daily new recovered
df['new_recovered'] = df.groupby('country')['recovered'].diff().fillna(0)

df['growth_rate_pct'] = df['new_cases'] / df.groupby('country')['cases'].shift(1)
df['growth_rate_pct'] = df['growth_rate_pct'].replace([float('inf'), -float('inf')], 0)
df['growth_rate_pct'] = df['growth_rate_pct'].fillna(0) * 100

df['new_cases_7day'] = df.groupby('country')['new_cases'].transform(lambda x:x.rolling(7,min_periods=1).mean())
df['new_deaths_7day'] = df.groupby('country')['new_deaths'].transform(lambda x:x.rolling(7,min_periods=1).mean())


# Rounding for cleaner File

df['growth_rate_pct'] = df['growth_rate_pct'].round(2)
df['new_cases_7day'] = df['new_cases_7day'].round(0)
df['new_deaths_7day'] = df['new_deaths_7day'].round(0)

# Fill any remaining NaN (should be none now)
df = df.fillna(0)


# Save clean version
df.to_csv('covid_clean.csv', index=False)
print("Transform complete! Saved to covid_clean.csv")
print("Columns now:", list(df.columns))
print("\nSample for USA (latest 5 days):")
print(df[df['country'] == 'USA'].tail(5)[['date', 'cases', 'new_cases', 'new_cases_7day', 'growth_rate_pct']])