from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

# BASE SETTINGS
class Settings(BaseSettings):
    """ENV VARIABLES SETTINGS"""
    DB_CONNECTION_URL: str
    ADMIN_TOKEN: str

    model_config = SettingsConfigDict(
        env_file="backend/.env",
        env_file_encoding="utf-8"
    )

# FUNCTION TO GET SETTINGS
@lru_cache()
def get_settings():
    return Settings()   # type: ignore

# CREATING INSTANCE OF SETTINGS
settings: Settings = get_settings()