from fastapi import APIRouter, Depends, UploadFile, File, status
from fastapi.responses import JSONResponse
import aiofiles

from models import ResponseSignal
from helper.config import get_settings, Settings
from controller import DataController, ProjectController
import logging

logger = logging.getLogger('uvicorn.error')

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api V1", "data"]
)

@data_router.post("/upload/{project_id}")
async def upload_data(
    project_id: str,
    file: UploadFile = File(...),
    app_settings: Settings = Depends(get_settings),
):
    data_controller = DataController()
    is_valid, res_signal = data_controller.validate_uploaded_file(file=file)

    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"signal": res_signal},
        )

    file_path = data_controller.gen_unique_filename(file.filename, project_id)
    try:

        async with aiofiles.open(file_path, "wb") as f:
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(chunk)
    except Exception as e :
        logger.error(f'Error while uploading file: {e}') # dont show the user all the thing dont be generice
        return JSONResponse(

            status_code= HTTP_400_BAD_REQUEST,
            content={'signal' : ResponseSignal.FILE_UPLOAD_FAILED.value}
        )

    return JSONResponse(content={"signal": ResponseSignal.FILE_UPLOAD_SUCCESS.value})
