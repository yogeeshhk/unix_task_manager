from fastapi import FastAPI

from src.task.router import router

app = FastAPI(title="Unix-Inspired Task Manager")

app.include_router(router, prefix="/tasks")


@app.get("/health")
def health_check():
    return {"status": "ok"}
