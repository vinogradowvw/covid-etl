from clickhouse_connect import get_async_client
from clickhouse_connect.driver.asyncclient import AsyncClient
import os


async def get_client() -> AsyncClient:

    ch_host: str = 'localhost' if os.getenv('CH_HOST') is None else str(os.getenv('CH_HOST'))
    if (os.getenv('CH_PORT') is None):
        ch_port: int = 8123
    elif (os.getenv('CH_HOST').isnumeric()):
        ch_port: int = int(os.getenv('CH_HOST'))
    else:
        raise TypeError("ClickHouse port environment variable must be a integer!")

    ch_user: str = 'default' if os.getenv('CH_USER') is None else str(os.getenv('CH_USER'))
    ch_pass: str = '' if os.getenv('CH_PASSWORD') is None else str(os.getenv('CH_PASSWORD'))

    client: AsyncClient = await get_async_client(port=ch_port,
                                                 host=ch_host,
                                                 user=ch_user,
                                                 password=ch_pass)
    return client
