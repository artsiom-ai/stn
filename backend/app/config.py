from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./saleslab.db"
    SECRET_KEY: str = "change-me-to-a-random-secret"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    LLM_PROVIDER_PRIMARY: str = "openai"
    LLM_PROVIDER_FALLBACK: str = "anthropic"
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    MAX_LLM_REQUESTS_PER_SESSION: int = 50
    MAX_MESSAGE_LENGTH: int = 1000
    USE_LLM: bool = True
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:5174,http://127.0.0.1:5173,http://127.0.0.1:5174"

    class Config:
        env_file = ".env"


settings = Settings()