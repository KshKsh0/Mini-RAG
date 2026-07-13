from pydantic_settings import BaseSettings , SettingsConfigDict
#this is for validation handling , no need to handle it manually this library can do it 
#also if i want to change something about the logic from .env  i can change it here so it good way to do it and important
from typing import List

class Settings(BaseSettings):
    APP_NAME:str
    APP_VERSION:str
    OPENAI_API_KEY:str
    GEMINI_API_KEY:str
    
    FILE_ALLOWED_TYPES:List[str]
    FILE_MAX_SIZE: int 
    FILE_DEFAULT_CHUNK_SIZE:int
    
    MONGODB_URL:str
    MONGODB_DATABASE:str
    
    GENERATION_BACKEND:str
    EMBEDDING_BACKEND:str
    OPENAI_API_URL:str = None
    COHERE_API_KEY:str     
    GENERATION_MODEL_ID:str = None
    EMBEDDING_MODEL_ID:str =None
    EMBEDDING_MODEL_SIZE:int =None
    INPUT_DAFUALT_MAX_CHARACTERS:int =None
    GENERATION_DAFUALT_MAX_TOKENS:int = None
    GENERATION_DAFUALT_TEMPERATURE:float =None

    VECTOR_DB_BACKEND:str = 'QDRANT'
    VECTOR_DB_PATH:str = 'qdrant_db'
    VECTOR_DB_DISTANCE_METHOD:str ='COSIN'
    DEFAULT_LANG :str = 'en'
    PRIMARY_LANG :str = 'en'
    

    class Config:
        env_file='.env' 

def get_settings():
    return Settings()