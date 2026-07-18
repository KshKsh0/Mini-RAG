# Mini-RAG
This is a minimal implementation of RAG system for question-answering

## Requirements 
- python 3.8 or later 


## Install Dependencies (linux)
```bash 

sudo apt update
sudo apt install libpq-dev gcc python3-dev
```
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

## Run Docker compose services 
```bash
$ cd docker 
$ cp .env.example .env
$ sudo docker compose up    
```
- update `.env` with you'r credentials
 


## Run FastAPI server
```bash
uvicorn main:App --reload  --port 8000
```

## Run Alembic Migration


### Configuration
```bash 
cp alembic.ini.example alembic.ini
```
- update the alembic.ini with you'r database credentials ('sqlalchemy.url)

### (Optional) Create new migration 

```bash
alembic revision --autogenerate -m 'ADD ..'
```

### Upgrade the database

```bash
alembic upgrade head
```
