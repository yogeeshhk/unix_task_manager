import logging
import os
from logging.handlers import RotatingFileHandler

from src.config import settings

LOG_FILE_PATH = settings.LOG_FILE_PATH
os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)

    if not logger.hasHandlers():
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        file_handler = RotatingFileHandler(
            LOG_FILE_PATH,
            maxBytes=204800,
            backupCount=0,
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        logger.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)

    return logger
