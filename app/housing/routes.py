from fastapi import APIRouter, Query, Header, HTTPException, status, Depends, Security
from security import verify_token, RateLimiter
from housing.enums import OceanProximityEnum
from housing.model import load_model, predict, MODEL_NAME
from housing.response_models import PredictOut
import pandas as pd

router = APIRouter()

@router.get(
    "/predict",
    response_model=PredictOut,
    responses={
        403: {"description": "Unauthorized - invalid or missing token"},
        429: {"description": "Rate limit exceeded"}
    }
)
def get_housing_price_prediction(
    longitude: float = Query(description="Longitude of the location"),
    latitude: float = Query(description="Latitude of the location"),
    housing_median_age: float = Query(ge=0, description="Median age of the housing"),
    total_rooms: float = Query(ge=0, description="Total number of rooms"),
    total_bedrooms: float = Query(ge=0, description="Total number of bedrooms"),
    population: float = Query(ge=0, description="Population of the area"),
    households: float = Query(ge=0, description="Number of households"),
    median_income: float = Query(ge=0, description="Median income of the area"),
    ocean_proximity: OceanProximityEnum = Query(description="Proximity to the ocean"),
    authorized: bool = Depends(verify_token),
    limited: bool = Depends(RateLimiter.verify_limit)
):
    df = pd.DataFrame([{
        'longitude': longitude,
        'latitude': latitude,
        'housing_median_age': housing_median_age,
        'total_rooms': total_rooms,
        'total_bedrooms': total_bedrooms,
        'population': population,
        'households': households,
        'median_income': median_income,
    } | {'ocean_proximity_' + op.value: 1 if op == ocean_proximity else 0 for op in OceanProximityEnum}])

    model = load_model(MODEL_NAME)
    return {"price": predict(df, model)[0]}