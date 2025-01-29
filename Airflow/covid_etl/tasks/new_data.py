from airflow.operators.python import PythonOperator


def extract_new_data():
    # TODO
    pass


def get_extract_new_data_task(dag):
    return PythonOperator(
        task_id='extract_new_data',
        python_callable=extract_new_data,
        dag=dag
    )
