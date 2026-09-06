from pydantic_settings import BaseSettings, SettingsConfigDict
from urllib.parse import quote_plus

#automatically reading environment variables if defined, else find it in .dev.env
class Settings(BaseSettings):
    database_url: str | None = None

    db_host: str | None = None
    db_port: int = 5432
    db_name: str | None = None
    db_username: str | None = None
    db_password: str | None = None
    environment: str = "development"

    #For local testing, file not included in the image
    model_config = SettingsConfigDict(
        env_file=".dev.env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    #Build database url
    def model_post_init(self, __context) -> None:
        if self.database_url is None:
            username = quote_plus(self.db_username)
            password = quote_plus(self.db_password)

            self.database_url = (
                f"postgresql+psycopg://"
                f"{username}:{password}"
                f"@{self.db_host}:{self.db_port}/{self.db_name}"
            )


settings = Settings()