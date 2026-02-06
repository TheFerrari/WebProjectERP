from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env.example', extra='ignore')
    fastapi_app_name: str = 'inventory-services'
    fastapi_debug: bool = False
    fastapi_database_url: str
    fastapi_jwt_secret: str
    fastapi_cors_origins: str = 'http://localhost:8000'


settings = Settings()
