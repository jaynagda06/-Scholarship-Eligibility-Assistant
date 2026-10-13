import os
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    DATABASE_URL: str = Field(default='sqlite:///scholarship.db', description='Database connection URL')
    OPENAI_API_KEY: str = Field(default='', description='OpenAI API key')
    OPENAI_MODEL: str = Field(default='gpt-4o-mini', description='OpenAI model name')
    CORS_ORIGINS: str = Field(default='http://localhost:5173', description='Comma-separated CORS origins')
    SEARCH_LIMIT: int = Field(default=50)
    MATCH_THRESHOLD: float = Field(default=0.0)

    class Config:
        env_file = '.env'

settings = Settings()
