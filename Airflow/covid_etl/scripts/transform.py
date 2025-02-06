import pandas as pd
import numpy as np
from datetime import datetime
from airflow.models import Variable

def _transform_2020_data():
    df = pd.read_csv('https://drive.google.com/uc?id=18Q2VzN9nVZl9CD6a4kC3JoETe4QCxS3h')

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

    return df.to_dict(orient='records')


def _transform_2024_data():
    df = pd.read_csv('https://srhdpeuwpubsa.blob.core.windows.net/whdh/COVID/WHO-COVID-19-global-daily-data.csv')

    # select only Russia
    df = df.loc[df['Country_code'] == 'RU']

    # drop all unnecessary columns
    df.drop(columns=['Country', 'WHO_region', 'Country_code', 'Cumulative_cases', 'Cumulative_deaths'], inplace=True)

    # transform data to datetime object
    df['Date_reported'] = df['Date_reported'].apply(lambda x: datetime.fromisoformat(x))

    # filter only actual data
    df = df.loc[df['Date_reported'] > datetime.fromisoformat('2020-12-14')]

    # rename columns
    df.rename(columns={'Date_reported': 'date', 'New_cases': 'cases', 'New_deaths': 'deaths'}, inplace=True)

    # filling null values for the weekly reports (after 15.05.2023)
    df = df.bfill().ffill()

    df_weekly = df.loc[df['date'] > datetime.fromisoformat('2023-05-15')]
    df.loc[df['date'] > datetime.fromisoformat('2023-05-15'), ['cases', 'deaths']] = df_weekly[['cases', 'deaths']] // 7

    # transform data back to string
    df['date'] = df['date'].apply(lambda x: x.strftime('%Y-%m-%d'))

    df = df.astype(int, errors='ignore')

    last_date = df['date'].to_list()[-1]
    Variable.set('last_data_date', last_date)

    return df.to_dict(orient='records')
