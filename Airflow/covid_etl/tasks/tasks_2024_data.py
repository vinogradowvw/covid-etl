from covid_etl.scripts.transform import _transform_2024_data
from covid_etl.scripts.load import load_records
from airflow.operators.python import PythonOperator


# transform 2024 data task
def transform_2024_data(ti):
    ti.xcom_push(key='2024_transformed_data', value=_transform_2024_data())


def get_transform_2024_task(dag):
    return PythonOperator(
        task_id='transform_2024_data',
        python_callable=transform_2024_data,
        dag=dag
    )


# load 2024 data task
def load_2024_data(ti):
    load_records(ti.xcom_pull(key='2024_transformed_data', task_ids='transform_2024_data'))


def get_load_2024_task(dag):
    return PythonOperator(
        task_id='load_2024_data',
        python_callable=load_2024_data,
        dag=dag
    )
