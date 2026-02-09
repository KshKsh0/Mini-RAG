from fastapi import APIRouter, Depends, UploadFile, File, status , Request
from fastapi.responses import JSONResponse
import aiofiles
from .schemes.data import PreprocessRequest
from models import ResponseSignal
from helper.config import get_settings, Settings
from controller import DataController, ProjectController , ProcessController
from models.ProjectModel import ProjectModel
from models.db_schemes import DataChunk
from models.ChunkModel import ChunkModel
import logging

logger = logging.getLogger('uvicorn.error')

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api V1", "data"]
)

@data_router.post("/upload/{project_id}")
async def upload_data(request : Request,
    project_id: str,
    file: UploadFile = File(...),
    app_settings: Settings = Depends(get_settings),
):

    project_model = await ProjectModel.create_instance(db_client= request.app.db_client)
    project = await project_model.get_project_or_create_one(project_id=project_id)
    data_controller = DataController()
    is_valid, res_signal = data_controller.validate_uploaded_file(file=file)

    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"signal": res_signal},
        )

    file_path , file_id  = data_controller.gen_unique_filepath(file.filename, project_id)
    try:

        async with aiofiles.open(file_path, "wb") as f:
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(chunk)
    except Exception as e :
        logger.error(f'Error while uploading file: {e}') # dont show the user all the thing dont be generice
        return JSONResponse(

            status_code= status.HTTP_400_BAD_REQUEST,
            content={'signal' : ResponseSignal.FILE_UPLOAD_FAILED.value}
        )

    return JSONResponse(content={"signal": ResponseSignal.FILE_UPLOAD_SUCCESS.value , 
    
    'file_id':file_id,
    
    })

@data_router.post('/process/{project_id}')
async def process_endpoint(project_id:str , process_request: PreprocessRequest, request : Request ):



    project_model = await ProjectModel.create_instance(db_client= request.app.db_client)
    project = await project_model.get_project_or_create_one(project_id=project_id)

    file_id = process_request.file_id
    chunk_size = process_request.chunk_size
    overlap= process_request.overlap
    do_reset = process_request.do_reset

    process_controller = ProcessController(project_id= project_id)
    file_content = process_controller.get_file_content(file_id=file_id)
    file_chunks = process_controller.process_file_content(chunk_size=chunk_size , 
                                                          file_id=file_id , overlap=overlap
                                                          , file_content=file_content)
    
    if file_chunks is None  or len(file_chunks) == 0:
            return JSONResponse(content={
                 "signal": ResponseSignal.PROCESSING_FAILED.value} )
    
    chunk_model = await ChunkModel.create_instance(db_client= request.app.db_client  )
         
    file_chunks_records = [
         DataChunk(chunk_text = chunk.page_content,
                   chunk_metadata= chunk.metadata, 
                   chunk_project_id=project.id,
                   chunk_order =i+1 
                   )
         for i, chunk in enumerate(file_chunks)
    ]


    if do_reset == 1:
         no_deleted = await chunk_model.delete_chunks_by_project_id(project_id = project.id)

    no_rec = await chunk_model.insert_many_chunk(chunks=file_chunks_records)
    return JSONResponse(content ={
         
            'signal':ResponseSignal.PROCESSING_SUCCESS.value,
            'inserted_chunks':no_rec,
            'num_deleted': no_deleted
    })
