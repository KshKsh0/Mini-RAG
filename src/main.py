from fastapi import FastAPI
from routes import base
#making main as short as possible 
App=FastAPI()
App.include_router(base.base_router)