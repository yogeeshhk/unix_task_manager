from sqlalchemy import text
from sqlalchemy.exc import OperationalError

from src.common.logger import get_logger
from src.db.database import SessionLocal

logger = get_logger(__name__)


def check_db_connection():
    try:
        with SessionLocal() as session:
            session.execute(text("SELECT 1"))
        return True
    except OperationalError as e:
        logger.error("Could not connect to the database.")
        logger.debug(f"Detailed DB error: {e}")
        return False
