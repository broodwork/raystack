from fastapi import FastAPI, Request

from cotlette import Cotlette

# Настройка логирования
import logging
logger = logging.getLogger("uvicorn")
logger.info("STARTED")
logger.warning("WARNING")
logger.error("ERROR")

app = Cotlette()
