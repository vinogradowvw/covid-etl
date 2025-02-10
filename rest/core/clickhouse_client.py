from clickhouse_connect import get_async_client
from clickhouse_connect.driver.asyncclient import AsyncClient
from dotenv import load_dotenv
import os
from pathlib import Path


async def get_client() -> AsyncClient:
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    env_path = BASE_DIR / ".env"
    load_dotenv(env_path)
    ch_host: str = 'localhost' if os.getenv('CH_HOST') is None else str(os.getenv('CH_HOST'))
    ch_port = os.getenv('CH_PORT')
    if (ch_port is None):
        ch_port: int = 8123
    elif (ch_port.isnumeric()):
        ch_port: int = int(ch_port)
    else:
        raise TypeError("ClickHouse port environment variable must be a integer!")

    ch_user: str = 'default' if os.getenv('CH_ADMIN_USER') is None else str(os.getenv('CH_ADMIN_USER'))
    ch_pass: str = '' if os.getenv('CH_ADMIN_PWD') is None else str(os.getenv('CH_ADMIN_PWD'))

    client: AsyncClient = await get_async_client(port=ch_port,
                                                 host=ch_host,
                                                 user=ch_user,
                                                 password=ch_pass)
    return client
