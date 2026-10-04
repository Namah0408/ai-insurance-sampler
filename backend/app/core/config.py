from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Insurance Sampler"
    app_version: str = "0.1.0"

    environment: str = "development"

    backend_host: str = "127.0.0.1"
    backend_port: int = 8000

    frontend_url: str = "http://localhost:5173"

    database_url: str = (
        "postgresql+psycopg://postgres:postgres@localhost:5432/"
        "ai_insurance_sampler"
    )

    tesseract_path: str = (
        r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    )

    document_storage_path: str = "storage/documents"
    max_document_size_mb: int = 10

    # ---------------------------------------------------------
    # External integrations
    # ---------------------------------------------------------

    integration_mock_mode: bool = True

    omnidocs_base_url: str = ""
    omnidocs_api_key: str = ""

    karza_base_url: str = ""
    karza_api_key: str = ""

    iib_base_url: str = ""
    iib_api_key: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()