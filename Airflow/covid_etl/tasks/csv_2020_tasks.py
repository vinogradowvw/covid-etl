from airflow.operators.python import PythonOperator
from covid_etl.scripts.CSV_2020.transform import transform
from covid_etl.scripts.CSV_2020.load import load_recods
from covid_etl.scripts.CSV_2020.extract import extract 

# Extract 2020 data
def get_extract_2020_task(dag):
    return PythonOperator(
        task_id='extract_2020_data',
        python_callable=extract,
        dag=dag
    )


# Transform old data from csv task
def transform_2020_data(ti):
    ti.xcom_push(key='2020_transformed_data', value=transform())


def get_transform_2020_task(dag):
    return PythonOperator(
        task_id='transform_2020_data',
        python_callable=transform_2020_data,
        dag=dag
    )


# Load old data to Kafka
def load_2020_data(ti):
    load_recods(ti.xcom_pull(key='2020_transformed_data', task_ids='transform_2020_data'))


def get_load_2020_task(dag):
    return PythonOperator(
        task_id='load_2020_data',
        python_callable=load_2020_data,
        dag=dag
    )
