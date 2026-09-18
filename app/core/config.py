from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    APP_NAME: str

    APP_VERSION: str

    HOST: str

    PORT: int

    DEBUG: bool

    FRONTEND_URL: str

    UPSTOX_BASE_URL: str
    
    UPSTOX_ACCESS_TOKEN: str

    TELEGRAM_BOT_TOKEN: str = ""
    TELEGRAM_CHAT_ID: str = ""
    TELEGRAM_ENABLED: bool = False

    class Config:
        env_file = ".env"

settings = Settings()