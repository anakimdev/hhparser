import os
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse

sys.path.insert(1, os.path.join(sys.path[0], '..'))

app = FastAPI(title="FastAPI")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
)


@app.get('/')
async def start_program():
    return f'Hello'
