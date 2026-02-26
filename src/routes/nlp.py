from fastapi import APIRouter, Depends, status , Request
import logging 
from controller import NLPController
from fastapi.responses import JSONResponse
from routes.schemes.nlp import PushRequest , SearchRequest
from models import ResponseSignal
from models.ProjectModel import ProjectModel
from models.ChunkModel import ChunkModel
logger = logging.getLogger('uvicorn.error')

nlp_router = APIRouter(

    prefix = '/api/v1/nlp',
    tags = ['api_v1' , 'nlp']
)

@nlp_router.post('/index/push/{project_id}')
async def index_project(request : Request , project_id:str ,push_request:PushRequest ):
    
    project_model = await ProjectModel.create_instance(db_client= request.app.db_client)


    project = await project_model.get_project_or_create_one(

        project_id = project_id
    )
    chunk_model = await ChunkModel.create_instance(
        db_client=request.app.db_client
    )

    if not project :
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = {

                'signal':ResponseSignal.PROJCT_NOT_FOUND_ERROR.value
            }
        )

    nlp_controller = NLPController(

        vectordb_clinet=request.app.vectordb_client,
        embedding_client=request.app.embedding_client,
        generatoin_client=request.app.generation_client
    )

    has_records = True
    page_no = 1
    page_size = 50
    inserted_item_count = 0

    while True:
        page_chunks = await chunk_model.get_project_chunk(
            project_id=project.id,
            page_no=page_no,
            page_size=page_size
        )

        if not page_chunks:
            break

        is_inserted = nlp_controller.index_into_vector_db(
            project=project,
            chunks=page_chunks,
            do_reset=push_request.do_reset and page_no == 1  # reset only once
        )

        if not is_inserted:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={'signal': ResponseSignal.INSERTED_TO_VECTOR_DB_ERROR.value}
            )

        inserted_item_count += len(page_chunks)
        page_no += 1

    return JSONResponse(
        content={
            'signal': ResponseSignal.INSERTED_TO_VECTOR_DB_SUCCESS.value,
            'inserted_item_count': inserted_item_count
        }
    )

        # chunks = chunk_model.get_project_chunks(project_id = project.project_id)


@nlp_router.get('/index/push/{project_id}')
async def get_project_index_info(request:Request , project_id:str):
    project_model = await ProjectModel.create_instance(db_client= request.app.db_client)


    project = await project_model.get_project_or_create_one(

        project_id = project_id
    )
    nlp_controller = NLPController(

        vectordb_clinet=request.app.vectordb_client,
        embedding_client=request.app.embedding_client,
        generatoin_client=request.app.generation_client
    )
    #not doc , it statues code different polymorphic
    collection_info =  nlp_controller.get_db_collection_info(project= project)
    print(collection_info)
    return JSONResponse(
        content = {

            'signal':ResponseSignal.VECTOR_COLLECTION_RETRIVED.value ,
            'collection_info': collection_info
        }
    )


@nlp_router.post('/index/search/{project_id}')
async def index_project(request:Request , project_id , search_request:SearchRequest):
     
     
    project_model = await ProjectModel.create_instance(db_client= request.app.db_client)


    project = await project_model.get_project_or_create_one(

        project_id = project_id
    )
    nlp_controller = NLPController(

        vectordb_clinet=request.app.vectordb_client,
        embedding_client=request.app.embedding_client,
        generatoin_client=request.app.generation_client
    )
    
    res = nlp_controller.search_vector_db_collection(
        project=project,
        texts= search_request.text,
        limit=search_request.limit
    )
    if not res:
         return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={'signal': ResponseSignal.INSERTED_TO_VECTOR_DB_ERROR.value}
            )


    return JSONResponse(
        content={

            'signal':ResponseSignal.VECTOR_SEARCH_DONE.value,
            'result' : res,
        })

