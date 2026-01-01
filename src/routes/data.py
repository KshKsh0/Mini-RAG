from fastapi import FastAPI,APIRouter ,Depends , UploadFile
from helper.config import get_settings , Settings

base_router=APIRouter(
    prefix='/api/v1/data', #making the access for the api start from this to all function below
    tags=['api V1' , 'data']

)

@base_router.post('/upload/{project_id}')
async def upload_data(project_id:str ,File:UploadFile, 
                      app_settings:Settings = Depends(get_settings()) ):
    pass