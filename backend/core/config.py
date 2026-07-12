from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    APP_NAME: str
    APP_VERSION: str
    DEBUG: bool

    DATABASE_URL: str

    GROQ_API_KEY: str = ""

    MODEL_PATH: str

    VECTOR_STORE_PATH: str

    DATASET_PATH: str

    class Config:
        env_file = ".env"


settings = Settings()