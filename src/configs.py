from pydantic_settings import BaseSettings
from pathlib import Path

ENV_PATH = Path(__file__).parent / ".env"

class Settings(BaseSettings):
    user_name: str 
    password: str 
    host: str 
    port: int 

    class Config:
        env_file = ENV_PATH


def get_settings():
    return Settings()
