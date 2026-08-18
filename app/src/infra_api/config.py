from pydantic_settings import BaseSettings, SettingsConfigDict

#automatically reading environment variables if defined, else find it in .dev.env
class Settings(BaseSettings):
    database_url: str
    environment: str = "development"

    model_config = SettingsConfigDict(
        env_file=".dev.env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()