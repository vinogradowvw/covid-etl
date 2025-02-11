from fastapi import APIRouter
from fastapi import Depends
from core.dependencies import get_covid_data_service
from security.header import validate_api_key
from services import CovidDataService
from datetime import date

router = APIRouter(dependencies=[Depends(validate_api_key)],
                   tags=["Covid Data"])


@router.get('/')
async def get_all_data(service: CovidDataService = Depends(get_covid_data_service)):
    """
    Returns all available data from database.
    """
    return await service.get_all_data(columns=['cases', 'deaths'])


@router.get('/cases')
async def get_all_cases(
    start: date | None = None,
    end: date | None = None,
    service: CovidDataService = Depends(get_covid_data_service),
):
    """
    Returns either all cases if start and end are not set,
    or cases in the time interval between start and end.
    """
    if (start is None) and (end is None):
        return await service.get_all_data(columns=['cases'])
    elif (start is not None) and (end is not None):
        return await service.get_data_by_time_interval(start, end, columns=['cases'])


@router.get('/deaths')
async def get_all_deaths(
    start: date | None = None,
    end: date | None = None,
    service: CovidDataService = Depends(get_covid_data_service),
):
    """
    Returns either all deaths if start and end are not set,
    or cases in the time interval between start and end.
    """
    if (start is None) and (end is None):
        return await service.get_all_data(columns=['deaths'])
    elif (start is not None) and (end is not None):
        return await service.get_data_by_time_interval(start, end, columns=['deaths'])


@router.get('/summary')
async def get_summary(
    service: CovidDataService = Depends(get_covid_data_service)
):
    """
    Returns statistical summary of all observed data
    """
    return await service.get_summary()
