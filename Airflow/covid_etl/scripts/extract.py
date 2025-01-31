import requests


def _extract_2020_data():

    url = "https://drive.google.com/uc?id=18Q2VzN9nVZl9CD6a4kC3JoETe4QCxS3h"
    output_path = "/opt/bitnami/airflow/dags/covid_etl/data/data_2020.csv"

    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(output_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
    else:
        print(f"Error: {response.status_code}")
