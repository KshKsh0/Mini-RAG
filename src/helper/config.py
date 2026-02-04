from pydantic_settings import BaseSettings , SettingsConfigDict
#this is for validation handling , no need to handle it manually this library can do it 
#also if i want to change something about the logic from .env  i can change it here so it good way to do it and important
from typing import List

class Settings(BaseSettings):
    APP_NAME:str
    APP_VERSION:str
    OPENAI_API_KEY:str
    
    FILE_ALLOWED_TYPES:List[str]
    FILE_MAX_SIZE: int 
    FILE_DEFAULT_CHUNK_SIZE:int
    
    MONGODB_URL:str
    MONGODB_DATABASE:str
    

    class Config:
        env_file='.env' 

def get_settings():
    return Settings()