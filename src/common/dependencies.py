from fastapi import Query
from pydantic import BaseModel


class PaginationParams(BaseModel):
    limit: int = Query(default=100, ge=1, le=1000, description="Max results to return")
    offset: int = Query(default=0, ge=0, description="How many items to skip")
