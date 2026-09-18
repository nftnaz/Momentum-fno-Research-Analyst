from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    APP_NAME: str = "NSE FnO AI Analyst"
    APP_VERSION: str = "1.0.0"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False

    FRONTEND_URL: str = "http://localhost:5173"

    UPSTOX_BASE_URL: str = "https://api.upstox.com"
    UPSTOX_ACCESS_TOKEN: str = ""

    TELEGRAM_BOT_TOKEN: str = ""
    TELEGRAM_CHAT_ID: str = ""
    TELEGRAM_ENABLED: bool = False

    CRON_SECRET: str = ""


settings = Settings()