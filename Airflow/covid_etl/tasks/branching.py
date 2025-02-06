from airflow.operators.python import BranchPythonOperator
from airflow.models import Variable
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
from airflow.models import Variable


# Check if the old data is loaded
def is_old_data_loaded():
    if (Variable.get('old_data_loaded', default_var=False)):
        return 'check_new_data'
    else:
        Variable.set('old_data_loaded', True)
        return 'transform_2020_data'


def get_branching_task(dag):
    return BranchPythonOperator(
        task_id='is_old_data_loaded',
        python_callable=is_old_data_loaded,
        dag=dag
    )


def check_for_new_data():
    res = requests.get('https://xn--90aivcdt6dxbc.xn--p1ai/stopkoronavirus/')
    soup = BeautifulSoup(res.content, 'html.parser')

    last_post = soup.find_all('a', 'u-material-card u-material-cards__card')[0]
    last_post_link = last_post.attrs['href']

    res = requests.get('https://xn--90aivcdt6dxbc.xn--p1ai/' + last_post_link)
    soup = BeautifulSoup(res.content, 'html.parser')
    header = str(soup.find('h3').contents[0]).strip().replace('\xa0', ' ')
    header = re.sub(r"[^а-яА-ЯёЁ0-9 ]", "", header)
    pattern = r"За (\d+)ю неделю (\d{4}) года (\d{2})(\d{2})(\d{2})(\d{2})(\d{4})"

    match = re.search(pattern, header)

    last_date = datetime.fromisoformat(Variable.get('last_data_date'))
    print(Variable.get('last_data_date'))

    week_first_day = datetime(int(match.group(2)),
                              int(match.group(4)),
                              int(match.group(3)))

    if (last_date < week_first_day):
        Variable.set('last_data_date', week_first_day.strftime('%Y-%m-%d'))
        print(week_first_day.strftime('%Y-%m-%d'))
        return 'extract_new_data'
    else:
        return 'end'


def get_checking_new_data_task(dag):
    return BranchPythonOperator(
        task_id='check_new_data',
        python_callable=check_for_new_data,
        dag=dag
    )
