from pydantic import BaseModel, root_validator
from typing import Dict, Optional

class PredictionRequest(BaseModel):
    text: Optional[str] = None
    link: Optional[str] = None

    @root_validator(pre=True)
    def text_or_link(cls, values):
        text, link = values.get("text"), values.get("link")
        if not text and not link:
            raise ValueError("Should provide text or link")
        return values
    
    
class PredictionResponse(BaseModel):
    final_prediction: str
    prediction_class: str
    user_input: str
    fake_score: float
    fake_percentage: float
    real_score: float
    real_percentage: float