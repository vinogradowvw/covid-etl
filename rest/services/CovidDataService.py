from pandas import DataFrame
from datetime import datetime, date
from datetime import timedelta
from scipy.stats import linregress
from repositories import CovidDataRepository


class CovidDataService():

    def __init__(self, repository: CovidDataRepository) -> None:
        self.__repository = repository

    async def get_data_by_time_interval(self,
                                        start: datetime,
                                        end: datetime,
                                        columns: list[str]
                                        ) -> dict:
        df = await self.__repository.find_by_time_interval(start, end, columns)
        return df.to_dict(orient="list")

    async def get_all_data(self, columns: list[str]) -> dict:
        df = await self.__repository.find_all(columns)
        return df.to_dict(orient="list")

    async def get_summary(self) -> dict:
        df = await self.__repository.find_all()
        summary = {}

        for column in df.columns:
            if column == 'date':
                continue
            max_idx = df[column].idxmax()
            max_row = df.iloc[max_idx]
            summary['max_' + column] = {'time': max_row['date'],
                                        'value': float(max_row[column])}
            min_idx = df[column].idxmin()
            min_row = df.iloc[min_idx]
            summary['min_' + column] = {'time': min_row['date'],
                                        'value': float(min_row[column])}

        summary['mean'] = df.drop(columns=['date']).mean().to_dict()

        summary['trends'] = self.__calculate_trends(df)
        return summary

    def __calculate_trends(self, df: DataFrame) -> dict:
        today = df["date"].max()
        time_ranges = {
            "last_6_months": today - timedelta(days=6 * 30),
            "last_year": today - timedelta(days=365),
            "last_2_years": today - timedelta(days=2 * 365),
        }

        trends = {}

        for column in df.columns:
            if column == "date":
                continue

            column_trends = {}

            for period, start_date in time_ranges.items():
                df_filtered = df[df["date"] >= start_date]
                if len(df_filtered) < 2:
                    column_trends[period] = None
                    continue

                x = (df_filtered["date"] - df_filtered["date"].min()).dt.days.to_numpy()
                y = df_filtered[column].to_numpy()

                slope, _, _, _, _ = linregress(x, y)
                column_trends[period] = slope

            trends[column] = column_trends

        return trends
