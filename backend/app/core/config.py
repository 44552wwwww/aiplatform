from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = {"env_file": ".env"}

    # Database (默认 SQLite 便于开发，生产通过 .env 切换 PostgreSQL)
    DATABASE_URL: str = "sqlite:///./insightforge.db"

    # LLM (Provider-agnostic)
    LLM_PROVIDER: str = "openai_compatible"
    LLM_BASE_URL: str = ""
    LLM_API_KEY: str = ""
    LLM_MODEL: str = "deepseek-chat"
    LLM_TIMEOUT: int = 120
    LLM_API_PATH: str = "/v1/chat/completions"

    # Auth
    SECRET_KEY: str = "change-me"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_ALGORITHM: str = "HS256"

    # App
    DEBUG: bool = True
    CORS_ORIGINS: str = "http://localhost:5173"

    @field_validator("LLM_BASE_URL")
    @classmethod
    def validate_llm_base_url(cls, v: str) -> str:
        if v:
            return v.rstrip("/")
        return v

    @field_validator("SECRET_KEY")
    @classmethod
    def validate_secret_key(cls, v: str) -> str:
        if v == "change-me":
            raise ValueError("SECRET_KEY must be changed from default 'change-me'")
        if len(v) < 16:
            raise ValueError("SECRET_KEY must be at least 16 characters")
        return v

    @field_validator("CORS_ORIGINS")
    @classmethod
    def validate_cors_origins(cls, v: str) -> str:
        return ",".join(o.strip() for o in v.split(",") if o.strip())


settings = Settings()
