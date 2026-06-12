from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite:///assignment.db"
    app_base_url: str = "http://localhost:8000"
    seed: int = 42

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
