from pydantic_settings import BaseSettings , SettingsConfigDict
#this is for validation handling , no need to handle it manually this library can do it 
#also if i want to change something about the logic from .env  i can change it here so it good way to do it and important

class Settings(BaseSettings):
    APP_NAME:str
    APP_VERSION:str
    OPENAI_API_KEY:str

    class Config:
        env_file='.env' 

def get_settings():
    return Settings()