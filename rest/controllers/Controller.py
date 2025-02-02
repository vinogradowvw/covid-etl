from fastapi import APIRouter
from fastapi import Depends
from core.dependencies import get_service
from services import Service

router = APIRouter()


@router.get('/')
async def get_all_data(service: Service = Depends(get_service)):
    return await service.get_all_data(columns=['cases'])

 
@router.get('/cases')
async def get_all_cases(
    start=None,
    end=None,
    service: Service = Depends(get_service),
):
    if (start is None) and (end is None):
        return await service.get_all_data(columns=['cases'])
    elif (start is not None) and (end is not None):
        return await service.get_data_by_time_interval(start, end, columns=['cases'])


@router.get('/deaths')
async def get_all_deaths(
    start=None,
    end=None,
    service: Service = Depends(get_service),
):
    if (start is None) and (end is None):
        return await service.get_all_data(columns=['deaths'])
    elif (start is not None) and (end is not None):
        return await service.get_data_by_time_interval(start, end, columns=['deaths'])


@router.get('/summary')
async def get_summary(
    service: Service = Depends(get_service)
):
    return await service.get_summary()
