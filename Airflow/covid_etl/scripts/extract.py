from bs4 import BeautifulSoup
from datetime import datetime
from datetime import timedelta
from airflow.models import Variable
import requests


def _extract_new_data():
    res = requests.get('https://xn--90aivcdt6dxbc.xn--p1ai/stopkoronavirus/')
    soup = BeautifulSoup(res.content, 'html.parser')

    last_post = soup.find_all('a', 'u-material-card u-material-cards__card')[0]
    last_post_link = last_post.attrs['href']

    res = requests.get('https://xn--90aivcdt6dxbc.xn--p1ai/' + last_post_link)
    soup = BeautifulSoup(res.content, 'html.parser')

    data = soup.find_all('tr')[1]

    cases = int(str(data.find_all('td')[3].contents[0]).strip())
    deaths = int(str(data.find_all('td')[4].contents[0]).strip())

    new_data = []

    last_date = datetime.fromisoformat(Variable.get('last_data_date'))
    for i in range(7):
        date = last_date + timedelta(days=i)
        new_data.append({
            'date': date.strftime('%Y-%m-%d'),
            'cases': cases // 7,
            'deaths': deaths // 7
        })

    Variable.set('last_data_date', new_data[-1]['date'])
    return new_data
