from fastapi import FastAPI

from src.task.router import router as task_router

app = FastAPI(title="Unix-Inspired Task Manager")

app.include_router(task_router, prefix="/tasks")


@app.get("/health")
def health_check():
    return {"status": "ok"}
