from fastapi import FastAPI
from routes import api_router

app = FastAPI(title="DSTE Acceptance Assignment API")

app.include_router(api_router)
