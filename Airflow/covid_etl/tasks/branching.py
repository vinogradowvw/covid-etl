from airflow.operators.python import BranchPythonOperator
from airflow.models import Variable


# Check if the old data is loaded
def is_old_data_loaded():
    if (Variable.get('old_data_loaded', default_var=False)):
        return 'extract_new_data'
    else:
        Variable.set('old_data_loaded', True)
        return 'extract_2020_data'


def get_branching_task(dag):
    return BranchPythonOperator(
        task_id='is_old_data_loaded',
        python_callable=is_old_data_loaded,
        dag=dag
    )
