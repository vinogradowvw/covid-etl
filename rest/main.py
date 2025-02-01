from fastapi import FastAPI
from controllers import router
from core.dependencies import lifespan

app = FastAPI(lifespan=lifespan)

app.include_router(router)
