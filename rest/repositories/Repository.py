import asyncio
from rest.core.dependencies import get_client
from datetime import datetime
from pandas.core.base import DataFrame
from typing import List


class Repository():

    def __init__(self) -> None:
        self.__client = asyncio.run(get_client())

    async def find_by_time_interval(self,
                                    time_start: datetime,
                                    time_end: datetime,
                                    columns: List[str]
                                    ) -> DataFrame:
        parameters = {'start': time_start,
                      'end': time_end}
        query = 'SELECT date, '
        for column in columns:
            query += f'{column}, '
        query = query[:-2]

        query += """
                 FROM covid.etl
                 WHERE date < {end:DateTime} AND date > {start:DateTime}
                 """
        return await self.__client.query_df(query=query, parameters=parameters)

    async def find_all(self, columns: List[str]) -> DataFrame:
        query = 'SELECT date, '
        for column in columns:
            query += f'{column}, '
        query = query[:-2]

        query += """
                 FROM covid.etl
                 """
        return await self.__client.query_df(query=query)
