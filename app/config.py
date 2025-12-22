from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent


class Settings(BaseSettings):
    OPENAI_API_KEY: str
    DATABASE_URL: str = f"sqlite:///{BASE_DIR}/history.db"
    UPLOAD_DIR: Path = BASE_DIR / "uploads"
    model_config = SettingsConfigDict(env_file="../.env", env_file_encoding="utf-8")

settings = Settings()
settings.UPLOAD_DIR.mkdir(exist_ok=True)