from pydantic_settings import BaseSettings
from typing import Optional
import pathlib
from .logger_config import logger

class Settings(BaseSettings):
    LLM_PROVIDER: Optional[str] = "openai"
    MODEL: Optional[str] = "gpt-4o-mini"
    EMBEDDING_MODEL: Optional[str] = "text-embedding-3-large"
    EMBEDDING_DIMENSION: Optional[int] = "1024"
    LLM_API_KEY: Optional[str] = "sk"
    SERP_API_KEY: Optional[str] = "0cc3c6362...."
    TAVILY_API_KEY: Optional[str] = "tvly..."
    OPENWEATHERMAP_API_KEY: Optional[str] = "d95d2b3bb6..."
    ALLOW_CACHE: Optional[str] = "False"
    ALLOW_TRANSACTION_STORAGE: Optional[str] = "True"
    LOGGER_LEVEL: Optional[str] = "INFO"

config_path = pathlib.Path(__file__).parent / ".env"
settings = Settings(_env_file=config_path, _env_file_encoding='utf-8')
logger.info(f"Settings loaded.")









