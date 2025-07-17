from fastapi import FastAPI
from routes import api_router

app = FastAPI(title="My Awesome API")

app.include_router(api_router)
