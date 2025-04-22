import os
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from src.auth.service import get_current_admin_user
from src.auth.models import User
from src.config import settings
from datetime import datetime

LOG_FILE = settings.LOG_FILE_PATH

router = APIRouter(tags=["Monitoring"])


@router.get("/healthcheck")
def healthcheck(admin: User = Depends(get_current_admin_user)):
    if not os.path.exists(LOG_FILE):
        return JSONResponse(content={"message": "Log file not found"}, status_code=404)

    with open(LOG_FILE, "r") as f:
        logs = f.readlines()[-20:]

    return {
        "timestamp": datetime.utcnow().isoformat(),
        "status": "ok",
        "log_entries": logs
    }
