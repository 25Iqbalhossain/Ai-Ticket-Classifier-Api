from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",          # <-- extra env থাকলেও crash করবে না
        case_sensitive=False,    # <-- DATA_PATH / data_path mismatch এও safe
    )

    APP_NAME: str = "AI Ticket API"
    DATABASE_URL: str
    MODEL_PATH: str = "app/services/model.pkl"

    # prefer using settings.data_path everywhere
    data_path: str = Field(
        default="/app/app/data/enhanced_customer_support_data.csv",
        alias="DATA_PATH",
    )


settings = Settings()
