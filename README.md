# ETL process. RestAPI.

## Project Description
The goal of the project is to create an ETL process to deliver data from different sources to a single repository. The main requirement for implementation is to create a system that is autonomous, scalable, so that its components are not directly dependent on each other and user intervention is minimal. RestAPI with API-key access system is implemented to provide data obtained through ETL process. The storage of incidence data is done in the ClickHouse database. PostgreSQL is used to store user data and metadata for AirFlow. Each component of the system resides in a docker container.

The entire system looks like the following:

<img width="1392" alt="image" src="https://github.com/user-attachments/assets/ad684ea0-3195-4dfb-85eb-dc50bb9a2f86" />


### ETL process:

AirFlow is used to execute scripts written to extract, transform, and upload data.
General principles:

* Old data is transformed using the Pandas library.
* Branching into 2 pipelines: loading old data (if not already loaded) and loading new data.
* All data after processing is sent in JSON serialisation to a Kafka topic, from which it is read using Kafka sink connector and sent to ClickHouse database

The following groups of shuffles are implemented:
- Branching Tasks (```BranchPythonOperator```).
    Checks if old data is loaded. If they are already loaded - the process starts checking for new data on the web page. Checking for new data and old data is done using AirFlow runtime variables.

- transform shuffle (```PythonOperator```).
    For old data, the Pandas library is used. Missing values are either filled with a past non-empty value. Data after 15.05.2023 stopped being delivered daily - instead, for a week, I decided to just divide those values by 7 and fill in the past week's daily data with those values. BeautifulSoup is used to parse the new data from the web page.

- ```load_data``` (```PythonOperator```).
    Loading all data from the previous shuffle, uses a single script for any data and is done through the Kafka broker and Kafka clickhouse sink connector.




The whole task graph is as follows:

<img width="944" alt="image" src="https://github.com/user-attachments/assets/83d2f3eb-be30-48b5-83d2-c52c8195a303" />


### RestAPI.

The application is written on the FastAPI framework. It uses a three-layer architecture - controllers, services and a data access layer (repositories).

The data access layer consists of two components:

```UserRepository``` and ```CovidDataRepository```, use SQLAlchemy with postgresql asyncpg DBAPI and asynchronous clickhouse client respectively.

The services layer also consists of two components using the same logic:
```UserService``` - user handling logic, user creation, password verification, token verification and token reissue.
```CodivDataRepository``` - working directly with COVID incidence data

Controllers:
```UserController``` - user registration, re-issue of api key.
```CovidDataController``` - Data Access. Authentication by API key in *x-key* header is used.


All components use Dependency Injection. The lifecycle of the SQLAlchemy session and ClickHouse client are managed within the FastAPI application lifecycle using the inbuilt ```lifespan``` mechanism.

Once launched, documentation will be available at http://localhost:8000/docs#/ or http://localhost:8000/redoc
