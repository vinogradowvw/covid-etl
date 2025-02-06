from airflow.operators.python import PythonOperator
from covid_etl.scripts.extract import _extract_new_data
from covid_etl.scripts.load import load_records


def extract_new_data(ti):
    ti.xcom_push(key='new_data', value=_extract_new_data())


def get_extract_new_data_task(dag):
    return PythonOperator(
        task_id='extract_new_data',
        python_callable=extract_new_data,
        dag=dag
    )


def load_new_data(ti):
    load_records(ti.xcom_pull(key='new_data', task_ids='extract_new_data'))


def get_load_new_data_task(dag):
    return PythonOperator(
        task_id='load_new_data',
        python_callable=load_new_data,
        dag=dag
    )
