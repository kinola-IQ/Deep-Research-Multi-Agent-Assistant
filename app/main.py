from fastapi import FastAPI
from app.system.utils.logger import register_http_logging
from app.system.model.model_loader import lifespan
from app.interface.routes import router
# fastapi object
app = FastAPI(lifespan=lifespan)

register_http_logging(app)
app.include_router(router, prefix="/v1")
