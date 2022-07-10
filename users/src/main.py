from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.routes import api_router

app = FastAPI()

app.include_router(api_router, prefix="/api")
