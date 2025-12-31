from fastapi import FastAPI
App=FastAPI()

@App.get('/welcome')
def welcome():
    return {'message' :'hello world'}