import os
from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

@app.get('/')
async def root():
    # azure app
    x = os.environ.get('TEST')
    return {'msg': x}

@app.get('/test')
async def root():
    # .env
    x = os.environ.get('MONGO_DB')
    return {'msg': x}