from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from repositories import Repository
from core.clickhouse_client import get_client
from services import Service


@asynccontextmanager
async def lifespan(app: FastAPI):
    client = await get_client()
    repository = Repository(client)
    service = Service(repository)

    app.state.client = client
    app.state.repository = repository
    app.state.service = service

    yield

    await client.close()


def get_service(request: Request):
    return request.app.state.service
