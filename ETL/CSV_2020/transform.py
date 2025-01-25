import pandas as pd
from datetime import datetime
import numpy as np

df = pd.read_csv('./Data/data_2020.csv')

df.replace(0, np.NaN, inplace=True)
df.ffill()

# select only Russia
df = df.loc[df['geoId'] == 'RU']

# drop all unnecessary columns
columns_to_drop = [
    'countriesAndTerritories',
    'geoId',
    'continentExp',
    'day',
    'month',
    'year',
    'Cumulative_number_for_14_days_of_COVID-19_cases_per_100000',
    'countryterritoryCode'
]
df.drop(columns=columns_to_drop, inplace=True)


# transforming date to timestamp and popData2019 to int
def transform(row):
    row['dateRep'] = datetime.fromisoformat('-'.join(row['dateRep'].split('/')[::-1])).timestamp()
    row['popData2019'] = int(row['popData2019'])
    return row


df = df.apply(transform, axis=1)
