"""Environment settings, amount tolerance, and OCR thresholds."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    gemini_api_key: str = ""
    firecrawl_api_key: str = ""
    db_path: str = "data/payproof.db"
    ocr_min_confidence: float = 0.80
    amount_tolerance_inr: str = "1.00"
    backend_host: str = "127.0.0.1"
    backend_port: int = 8000
    frontend_origin: str = "http://localhost:3000"


settings = Settings()
