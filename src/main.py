from fastapi import FastAPI

from src.common.exception_handler import register_exception_handlers
from src.common.logger import get_logger
from src.auth.router import router as auth_router
from src.common.router import router as common_router
from src.db.utils import check_db_connection
from src.task.router import router as task_router

app = FastAPI(title="Unix-Inspired Task Manager")

register_exception_handlers(app)

app.include_router(auth_router)
app.include_router(task_router)
app.include_router(common_router)

logger = get_logger(__name__)


@app.on_event("startup")
def verify_db_on_startup():
    if not check_db_connection():
        logger.critical("Database connection failed during startup.")
        raise RuntimeError("Database is not available.")
