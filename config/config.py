from pydantic import BaseSettings


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str
    JWT_SECRET_KEY: str
    JWE_SECRET_KEY: str
    ACCESS_TOKEN_EXPIRY_TIME_MINUTES: int

    class Config:
        env_file = ".env"


settings = Settings()  # type: ignore
