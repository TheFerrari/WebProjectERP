from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = 'Inventory Services'
    debug: bool = False
    database_url: str
    jwt_secret: str
    allowed_origins: str = 'http://localhost:8000'

    class Config:
        env_prefix = 'FASTAPI_'
        case_sensitive = False

settings = Settings(
    database_url=__import__('os').getenv('DATABASE_URL', 'postgresql+psycopg://inventory_user:inventory_pass@localhost:5432/inventory_db'),
    jwt_secret=__import__('os').getenv('FASTAPI_JWT_SECRET', 'secret')
)
