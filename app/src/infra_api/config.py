from pydantic_settings import BaseSettings, SettingsConfigDict

#automatically reading environment variables if defined, else find it in .devenv
class Settings(BaseSettings):
    database_url: str
    environment: str = "development"

    model_config = SettingsConfigDict(
        env_file=".devenv",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()