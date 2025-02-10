from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import async_sessionmaker
import os
from pathlib import Path


async def get_postrgesql_session():
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    env_path = BASE_DIR / '.env'
    load_dotenv(env_path)
    pg_host: str = 'localhost' if os.getenv('PG_HOST') is None else str(os.getenv('PG_HOST'))

    pg_port = os.getenv('PG_PORT')
    if pg_port is None:
        pg_port = 5432
    elif pg_port.isnumeric():
        pg_port = int(pg_port)
    else:
        raise Exception('PostgreSQL port environment variable must be numeric')

    pg_user: str = 'postgres' if os.getenv('PG_ADMIN_USER') is None else str(os.getenv('PG_ADMIN_USER'))
    pg_pass: str = 'postgres' if os.getenv('PG_ADMIN_PWD') is None else str(os.getenv('PG_ADMIN_PWD'))

    url = URL.create(drivername='postgresql+asyncpg',
                     host=pg_host,
                     port=pg_port,
                     username=pg_user,
                     password=pg_pass,
                     database='auth')

    engine = create_async_engine(url)

    sessionmaker = async_sessionmaker(engine)

    async with sessionmaker() as session:
        return session
