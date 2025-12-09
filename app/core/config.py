from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "CRM Telegram"
    debug: bool = False

    database_url: str = "postgresql+asyncpg://user:password@localhost:5432/crm_telegram"
    secret_key: str = "CHANGE_ME"
    access_token_expire_minutes: int = 60 * 24

    static_dir: str = "static"
    templates_dir: str = "templates"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
