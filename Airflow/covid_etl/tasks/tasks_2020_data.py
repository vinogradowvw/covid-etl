from airflow.operators.python import PythonOperator
from covid_etl.scripts.extract import _extract_2020_data
from covid_etl.scripts.load import load_records
from covid_etl.scripts.transform import _transform_2020_data


# Transform old data from csv task
def transform_2020_data(ti):
    ti.xcom_push(key='2020_transformed_data', value=_transform_2020_data())


def get_transform_2020_task(dag):
    return PythonOperator(
        task_id='transform_2020_data',
        python_callable=transform_2020_data,
        dag=dag
    )


# Load old data to Kafka
def load_2020_data(ti):
    load_records(ti.xcom_pull(key='2020_transformed_data', task_ids='transform_2020_data'))


def get_load_2020_task(dag):
    return PythonOperator(
        task_id='load_2020_data',
        python_callable=load_2020_data,
        dag=dag
    )
