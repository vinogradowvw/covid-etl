from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from repositories import CovidDataRepository
from core.clickhouse_client import get_client
from core.postgresql_session import get_postrgesql_session
from repositories import UserRepository
from services import UserService
from services import CovidDataService


@asynccontextmanager
async def lifespan(app: FastAPI):
    click_house_client = await get_client()
    covid_data_repository = CovidDataRepository(click_house_client)
    postresql_session = await get_postrgesql_session()
    user_repository = UserRepository(postresql_session)

    covid_data_service = CovidDataService(covid_data_repository)
    user_service = UserService(user_repository)

    app.state.click_house_client = click_house_client
    app.state.covid_data_service = covid_data_service
    app.state.user_service = user_service
    app.state.postresql_session = postresql_session

    yield

    await app.state.click_house_client.close()
    await app.state.postresql_session.close()


def get_covid_data_service(request: Request):
    return request.app.state.covid_data_service


def get_user_service(request: Request):
    return request.app.state.user_service
