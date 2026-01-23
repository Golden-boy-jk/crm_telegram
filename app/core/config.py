from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "CRM Telegram"
    debug: bool = False

    db_host: str = Field("localhost", alias="DB_HOST")
    db_port: int = Field(5432, alias="DB_PORT")
    db_name: str = Field("crm_telegram", alias="DB_NAME")
    db_user: str = Field("user", alias="DB_USER")
    db_password: str = Field("password", alias="DB_PASSWORD")

    secret_key: str = Field("CHANGE_ME", alias="SECRET_KEY")
    access_token_expire_minutes: int = 60 * 24

    static_dir: str = "static"
    templates_dir: str = "templates"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  #чтобы лишние env не валили запуск
    )

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


settings = Settings()
