from fastapi import FastAPI
from controllers.CovidDataController import router as data_router
from controllers.UserController import router as user_router
from core.dependencies import lifespan

app = FastAPI(lifespan=lifespan)

app.include_router(data_router)
app.include_router(user_router)
