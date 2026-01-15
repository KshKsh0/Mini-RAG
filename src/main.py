from fastapi import FastAPI
from routes import base ,data
#making main as short as possible 
App=FastAPI()
App.include_router(base.base_router)
App.include_router(data.data_router)