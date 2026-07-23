from fastapi import FastAPI
from routes import base ,data , nlp
from helper.config import get_settings
from stores.LLM.LLMProviderFactory import LLMProviderFactory
from stores.vectordb.VectorDBProviderFactory import VectorDBProviderFactory
from stores.LLM.templates.template_parser import TemplateParser
from sqlalchemy.ext.asyncio import create_async_engine , AsyncSession
from sqlalchemy.orm import sessionmaker
#making main as short as possible 
App=FastAPI()


async def startup_span():
    settings= get_settings()
    
    postgres_conn = (
        f"postgresql+asyncpg://"
        f"{settings.POSTGRES_USERNAME}:"
        f"{settings.POSTGRES_PASSWORD}@"
        f"{settings.POSTGRES_HOST}:"
        f"{settings.POSTGRES_PORT}/"
        f"{settings.POSTGRES_MAIN_DATABASE}")    
    
    App.db_engine = create_async_engine(postgres_conn)
    
    App.db_client = sessionmaker(App.db_engine, class_=AsyncSession, 
                                 
                                 expire_on_commit=False
                                 
                                 )
    
    

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
    App.template_parser = TemplateParser(
        language=settings.PRIMARY_LANG
        ,default_language= settings.DEFAULT_LANG
    )

async def shutdown_span():
    App.db_engine.dispose()
    App.vectordb_client.disconnect()
    


# App.router.lifespan.on_startup.append(startup_span)
# App.router.lifespan.on_shutdown.append(shutdown_span)
App.on_event('startup')(startup_span)
App.on_event('shutdown')(shutdown_span)
App.include_router(base.base_router)
App.include_router(data.data_router)
App.include_router(nlp.nlp_router)