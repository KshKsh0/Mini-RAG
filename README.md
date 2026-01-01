# Mini-RAG
This is a minimal implementation of RAG system for question-answering

## Requirements 
- python 3.8 or later 

## installation

### install the reqiuerments
```bash
pip install requierments.txt
```

## set up the env file
``` bash
cp .env.example .env 
```
then set up you'r variables in the env file , like OPEN_API_KEY  value 

## Run FastAPI server
```bash
uvicorn main:App --reload  --port 8000
```
