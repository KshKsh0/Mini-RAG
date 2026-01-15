from fastapi import FastAPI,APIRouter ,Depends , UploadFile,status
from fastapi.responses import JSONResponse
from helper.config import get_settings , Settings
from controller import DataController , ProjectController
data_router=APIRouter(
    prefix='/api/v1/data', #making the access for the api start from this to all function below
    tags=['api V1' , 'data']

)

@data_router.post('/upload/{project_id}')
async def upload_data(project_id:str ,File:UploadFile, 
                      app_settings:Settings = Depends(get_settings) ):
     #validate file types  cause it logic we will do it in the controller folder
     is_valid,res_signal=  DataController().validate_uploaded_file(file =  File)
     

     if not is_valid:
          return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,content = {'signal':res_signal})
     project_dir=ProjectController().get_project_path(project_id = project_id)
     return is_valid , res_signal