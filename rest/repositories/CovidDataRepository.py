from datetime import date
from pandas import DataFrame
from typing import List
from repositories.Repository import Repository


class CovidDataRepository(Repository):

    async def find_by_time_interval(self,
                                    time_start: date,
                                    time_end: date,
                                    columns: List[str] = ['deaths', 'cases']
                                    ) -> DataFrame:
        parameters = {'start': time_start,
                      'end': time_end}
        query = 'SELECT date, '
        for column in columns:
            query += f'{column}, '
        query = query[:-2]

        query += """
                 FROM covid.etl
                 WHERE date < {end:Date} AND date > {start:Date}
                 """
        return await self.client.query_df(query=query, parameters=parameters)

    async def find_all(self,
                       columns: List[str] = ['deaths', 'cases']
                       ) -> DataFrame:
        query = 'SELECT date, '
        for column in columns:
            query += f'{column}, '
        query = query[:-2]

        query += """
                 FROM covid.etl
                 """
        return await self.client.query_df(query=query)
