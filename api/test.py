# import os
from fastapi import FastAPI


app = FastAPI()

@app.get('/')
async def root():
    # x = os.environ.get('TEST')
    return {'msg': 'hey'}