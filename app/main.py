"""main module"""
from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn

from app.system.utils.logger import register_http_logging
from app.system.model.model_loader import load_model
from app.interface.routes import router
from app.system.utils.logger import logger


# helper funciton to load model on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    # model
    # Run the blocking load_model in a separate thread so the event loop is not blocked
    await load_model()
    logger.info('model loaded successfully')
    yield


# fastapi object
def create_app():
    app = FastAPI(lifespan=lifespan)

    register_http_logging(app)
    app.include_router(router, prefix="/v1")
    return app


server = create_app()

if __name__ == "__main__":
    uvicorn.run('app.main:server', host="127.0.0.1", port=8000)
