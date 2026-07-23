from fastapi import FastAPI,APIRouter ,Depends
from helper.config import get_settings , Settings

base_router=APIRouter(
    prefix='/api/v1', #making the access for the api start from this to all function below
    tags=['api V1']
)

@base_router.get('/')
async def welcome(app_settings:Settings = Depends(get_settings)):
    # app_settings= get_settings()  more effient using Depends
    app_name=app_settings.APP_NAME
    app_version=app_settings.APP_VERSION
    return {'app name' :app_name , 'app version':app_version}