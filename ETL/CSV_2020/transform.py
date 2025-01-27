import pandas as pd
from datetime import datetime
import numpy as np

df = pd.read_csv('./Data/data_2020.csv')

df.replace(0, np.nan, inplace=True)
df.ffill(inplace=True)

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
    'countryterritoryCode',
    'popData2019'
]

df.drop(columns=columns_to_drop, inplace=True)


# transforming date to timestamp and popData2019 to int

df = df.astype(int, errors='ignore')


def transform_to_timestamp(time_str):
    return '-'.join(time_str.split('/')[::-1])


df['dateRep'] = df.apply(lambda x: transform_to_timestamp(x['dateRep']), axis=1)

# rename columns
df.rename(columns={'dateRep': 'date'}, inplace=True)
