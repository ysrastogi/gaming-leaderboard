from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./test.db"
    MAX_RECORDS: int = 1000000
    API_V1_STR: str = "/api/v1"

    class Config:
        env_file = ".env"

settings = Settings()