import requests
import pandas as pd
import json


#API Endpoint for historical data
url = "https://disease.sh/v3/covid-19/historical?lastdays=all"

print("Fetching Data")

response = requests.get(url)
if response.status_code != 200:
    print("Error: Could not fetch data. Status code:", response.status_code)
    exit()
    
data = response.json()

# build a list of rows for the DataFrame
rows = []


print("Processing data for each country...")
for country_data in data:
    country = country_data['country']
    timeline = country_data['timeline']
    
    cases = timeline['cases']
    deaths = timeline['deaths']
    recovered = timeline.get('recovered', {})  # Some might not have recovered
    
    for date, case_count in cases.items():
        row = {
            'country': country,
            'date': date,
            'cases': case_count,
            'deaths': deaths.get(date, 0),
            'recovered': recovered.get(date, 0)
        }
        rows.append(row)


# Create DataFrame
df = pd.DataFrame(rows)

# Convert date to proper datetime
df['date'] = pd.to_datetime(df['date'])

# Sort by country and date
df = df.sort_values(['country', 'date'])

# Save to CSV
df.to_csv('covid_raw.csv', index=False)
print("Done! Saved to covid_raw.csv")
print("Total rows:", len(df))
print("Countries:", df['country'].nunique())
print(df.head())
