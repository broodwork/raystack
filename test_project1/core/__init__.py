# from pydantic import BaseModel
# from cotlette.models import Model
# from cotlette.fields import CharField, IntegerField
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

from cotlette import Cotlette

# Настройка логирования
import logging
logger = logging.getLogger("uvicorn")
logger.info("STARTED")
logger.warning("WARNING")
logger.error("ERROR")

# Создаем экземпляр FastAPI
app = Cotlette()

# Подключение urls
# from config.urls import router as urls_router
# app.include_router(urls_router)

# Подключение директории static
app.mount("/static", StaticFiles(directory="static"), name="static")



