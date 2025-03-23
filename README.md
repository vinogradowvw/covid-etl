# ETL process. RestAPI.

## Project Description
The goal of the project is to create an ETL process to deliver data from different sources to a single repository. The main requirement for implementation is to create a system that is autonomous, scalable, so that its components are not directly dependent on each other and user intervention is minimal. RestAPI with API-key access system is implemented to provide data obtained through ETL process. The storage of incidence data is done in the ClickHouse database. PostgreSQL is used to store user data and metadata for AirFlow. Each component of the system resides in a docker container.

The entire system looks like the following:

<img width="1392" alt="image" src="https://github.com/user-attachments/assets/ad684ea0-3195-4dfb-85eb-dc50bb9a2f86" />


### ETL process:

AirFlow is used to execute scripts written to extract, transform and upload data.

General principles:

* Old data is transformed using the Pandas library.
* Branching into 2 pipelines: loading old data (if not already loaded) and loading new data.
* All data after processing is sent in JSON serialisation to a Kafka topic, from which it is read using Kafka sink connector and sent to ClickHouse database

The following groups of shuffles are implemented:
- Branching Tasks (```BranchPythonOperator``).
    Checks if old data is loaded. If it is already loaded, the process starts branching the old data.

Translated with DeepL.com (free version)
