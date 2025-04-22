from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from src.auth.router import router as auth_router
from src.common.exception_handler import register_exception_handlers
from src.common.logger import get_logger
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


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Unix Task Manager API",
        version="1.0.0",
        description="Because to-do lists weren’t stressful enough.",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }

    # Add security globally (optional, or per route)
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            openapi_schema["paths"][path][method]["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
