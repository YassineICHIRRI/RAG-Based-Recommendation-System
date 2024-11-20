from pydantic_settings import BaseSettings

from src import configs

class Settings(BaseSettings):
    user_name: str 
    password: str 
    host: str 
    port: int 


    class Config:
        env_file = configs.ENV_PATH

settings = Settings()


print(settings.password)
