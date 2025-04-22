from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    DATABASE_URL: str
    DEBUG: bool = False
    HASH_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    LOG_FILE_PATH: str = "logs/api.log"
    SECRET_KEY: str

    class Config:
        env_file = ".env"


settings = Settings()
