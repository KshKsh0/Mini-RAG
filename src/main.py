from fastapi import FastAPI
from routes import base ,data
from motor.motor_asyncio import AsyncIOMotorClient
from helper.config import get_settings
#making main as short as possible 
App=FastAPI()
@App.on_event('startup')
async def startup_db_client():
    settings= get_settings()
    App.mongo_conn=AsyncIOMotorClient(settings.MONGODB_URL)
    App.db_client = App.mongo_conn[settings.MONGODB_DATABASE]

@App.on_event('shutdown')
async def shutdown_db_client():
    App.mongo_conn.close()
    
App.include_router(base.base_router)
App.include_router(data.data_router)