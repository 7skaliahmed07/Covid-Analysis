import pandas as pd
df = pd.read_csv('covid_raw.csv')
print(sorted(df['country'].unique()))