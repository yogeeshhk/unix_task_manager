from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import relationship

from src.db.database import Base
from src.task.constants import TaskStatus
from src.auth.models import User


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    status = Column(SqlEnum(TaskStatus), default=TaskStatus.RUNNING, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime, default=datetime.utcnow, nullable=True)
    ended_at = Column(DateTime, nullable=True)

    parent_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)
    children = relationship("Task", remote_side=[id], backref="parent")

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", backref="tasks")
