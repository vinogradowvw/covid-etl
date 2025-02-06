from airflow import DAG
from airflow.operators.empty import EmptyOperator
from covid_etl.tasks.branching import get_branching_task
from covid_etl.tasks.tasks_2020_data import get_transform_2020_task
from covid_etl.tasks.tasks_2020_data import get_load_2020_task
from covid_etl.tasks.tasks_new_data import get_extract_new_data_task
from datetime import datetime
from covid_etl.tasks.tasks_2024_data import get_transform_2024_task
from covid_etl.tasks.tasks_2024_data import get_load_2024_task
from covid_etl.tasks.branching import get_checking_new_data_task
from covid_etl.tasks.tasks_new_data import get_load_new_data_task

with DAG(
    dag_id='covid_etl',
    start_date=datetime.now(),
    schedule='@daily',
    catchup=False,
    max_active_runs=1,
) as dag:

    branching = get_branching_task(dag)

    # 2020 data pipeline
    transform_2020 = get_transform_2020_task(dag)
    load_2020 = get_load_2020_task(dag)

    # 2024 data pipeline
    transform_2024 = get_transform_2024_task(dag)
    load_2024 = get_load_2024_task(dag)

    # New Data
    check_new_data = get_checking_new_data_task(dag)
    extract_new_data = get_extract_new_data_task(dag)
    load_new_data = get_load_new_data_task(dag)
    # End task
    end = EmptyOperator(task_id='end')

    branching >> [check_new_data, transform_2020]
    transform_2020 >> load_2020 >> transform_2024 >> load_2024

    check_new_data >> [extract_new_data, end]
    extract_new_data >> load_new_data
