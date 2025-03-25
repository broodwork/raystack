import os
import logging
# import importlib.util
import importlib

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from cotlette.conf import settings


__version__ = "0.0.0"

logger = logging.getLogger("uvicorn")


class Cotlette(FastAPI):

    def __init__(self):
        super().__init__()

        self.settings = settings
        
        # Подключение роутеров
        self.include_routers()
        
        # Получить абсолютный путь к текущей диретории
        current_file_path = os.path.abspath(__file__)
        current_directory = os.path.dirname(current_file_path)
        static_directory = os.path.join(current_directory, "static")
        self.mount("/static", StaticFiles(directory=static_directory), name="static")

    def include_routers(self):

        # # Подключаем роутеры к приложению
        # from cotlette.urls import urls_router, api_router
        # self.include_router(urls_router)
        # self.include_router(api_router, prefix="/api", tags=["common"],)

        # Проверка и импорт установленных приложений
        logger.info(f"Loading apps and routers:")
        for app_path in self.settings.INSTALLED_APPS:
            try:
                # Динамически импортируем модуль
                module = importlib.import_module(app_path)
                logger.info(f"✅'{app_path}': Successfully app loaded")

                # Если модуль содержит роутеры, подключаем их
                if hasattr(module, "router"):
                    self.include_router(module.router)
                    logger.info(f"✅'{app_path}': Successfully router included")
                else:
                    logger.warning(f"⚠️ '{app_path}': Not found router for module")
            except Exception as e:
                logger.error(f"❌'{app_path}': {str(e)}")
