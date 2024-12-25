from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    VIDEO_CATALOG: str

    class Config:
        env_file = ".env"


settings = Settings()
