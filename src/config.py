from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    JWT_SECRET_KEY: str
    JWT_ACCESS_COOKIE_NAME: str = "my_access_token"
    DATABASE_URL: str
    DEBUG: bool = False

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()