from fastapi import FastAPI,APIRouter
import os

base_router=APIRouter(
    prefix='/api/v1', #making the access for the api start from this to all function below
    tags=['api V1']
)

@base_router.get('/')
async def welcome():
    app_name=os.getenv('APP_NAME')
    app_version=os.getenv('APP_VERSION')
    return {'app name' :app_name , 'app version':app_version}