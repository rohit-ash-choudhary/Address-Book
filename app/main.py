import logging
import sys
from fastapi import FastAPI

from .config import LOG_LEVEL
from .database import engine
from . import models
from .routes import router

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    stream=sys.stdout,
)
app = FastAPI(title="Address Book", version="1.0.0")

@app.on_event("startup")
def startup():
    models.Base.metadata.create_all(bind=engine)

app.include_router(router)
