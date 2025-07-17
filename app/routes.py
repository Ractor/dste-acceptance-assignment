from fastapi import APIRouter
from housing.routes import router as housing_router

api_router = APIRouter()

api_router.include_router(housing_router, prefix="/housing", tags=["Housing"])
