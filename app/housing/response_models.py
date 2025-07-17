from pydantic import BaseModel, Field

class PredictOut(BaseModel):
    """
    Response model for housing price predictions.
    """
    price: float = Field(description="Predicted median house value")
    