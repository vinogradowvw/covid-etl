from airflow import DAG
from covid_etl.tasks.branching import get_branching_task
from covid_etl.tasks.csv_2020_tasks import get_extract_2020_task
from covid_etl.tasks.csv_2020_tasks import get_transform_2020_task
from covid_etl.tasks.csv_2020_tasks import get_load_2020_task
from covid_etl.tasks.new_data import get_extract_new_data_task
from datetime import datetime

with DAG(
    dag_id='covid_etl',
    start_date=datetime.now(),
    schedule='@daily',
    catchup=False,
    max_active_runs=1,
) as dag:

    branching = get_branching_task(dag)

    # 2020 data pipeline
    extract_2020 = get_extract_2020_task(dag)
    transform_2020 = get_transform_2020_task(dag)
    load_2020 = get_load_2020_task(dag)

    # New Data
    extract_new_data = get_extract_new_data_task(dag)

    branching >> [extract_new_data, extract_2020]
    extract_2020 >> transform_2020 >> load_2020
