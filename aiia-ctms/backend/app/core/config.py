from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=str(BACKEND_DIR / ".env"), extra="ignore")

    APP_NAME: str = "AIIA Clinical Trials Dashboard"
    APP_VERSION: str = "1.1.0"
    DB_FILE: str = str(BACKEND_DIR / "db.json")

    SECRET_KEY: str = "SUPER_SECRET_KEY_2026"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    DEMO_USER_EMAIL: str = "vansh@example.com"
    DEMO_USER_PASSWORD: str = "changeme123"

    OLLAMA_BASE_URL: str = "http://127.0.0.1:11434"
    PRIMARY_MODEL: str = "gemma4:31b-cloud"
    FALLBACK_MODEL: str = "mistral:latest"
    CODING_MODEL: str = "qwen3-coder-next:cloud"

    ALLOWED_ORIGINS: list[str] = ["*"]

settings = Settings()
