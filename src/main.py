from fastapi import FastAPI
from routes import base ,data , nlp
from motor.motor_asyncio import AsyncIOMotorClient
from helper.config import get_settings
from stores.LLM.LLMProviderFactory import LLMProviderFactory
from stores.vectordb.VectorDBProviderFactory import VectorDBProviderFactory
#making main as short as possible 
App=FastAPI()


async def startup_span():
    settings= get_settings()
    App.mongo_conn=AsyncIOMotorClient(settings.MONGODB_URL)
    App.db_client = App.mongo_conn[settings.MONGODB_DATABASE]

    llm_provier_factory = LLMProviderFactory(settings)
    vector_db_provider_factory = VectorDBProviderFactory(settings)
    
    #generatoin client 
    App.generation_client = llm_provier_factory.create(settings.GENERATION_BACKEND)
    App.generation_client.set_generation_model(model_id = settings.GENERATION_MODEL_ID)
    
   
    #embedding client 
    App.embedding_client = llm_provier_factory.create(settings.EMBEDDING_BACKEND)
    App.embedding_client.set_embedding_model(model_id = settings.EMBEDDING_MODEL_ID , embedding_size = settings.EMBEDDING_MODEL_SIZE)

    # vector db client 
    App.vectordb_client  = vector_db_provider_factory.create(provider= settings.VECTOR_DB_BACKEND  )

    App.vectordb_client.connect()

async def shutdown_span():
    App.mongo_conn.close()
    App.vectordb_client.disconnect()
    


# App.router.lifespan.on_startup.append(startup_span)
# App.router.lifespan.on_shutdown.append(shutdown_span)
App.on_event('startup')(startup_span)
App.on_event('shutdown')(shutdown_span)
App.include_router(base.base_router)
App.include_router(data.data_router)
App.include_router(nlp.nlp_router)