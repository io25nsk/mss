from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_PREFIX: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    JWT_KEY: str
    JWT_ALGORITHM: str
    JWT_TOKEN_EXPIRE_TIME: int

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
