from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI
from repositories import Repository
from core.clickhouse_client import get_client
from services import Service


repository = Repository(client=Depends(get_client))


def get_repository():
    return repository


service = Service(repository=Depends(get_repository))


def get_service():
    return service


@asynccontextmanager
async def lifespan(app: FastAPI):

    app.state.client = get_repository().client

    yield

    await app.state.client.close()
