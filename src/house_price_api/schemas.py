from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional

class PredictRequest(BaseModel):
    record: Dict[str, Any] = Field(..., description="Single record (feature dict).")

class PredictResponse(BaseModel):
    prediction: float
    model_version: str

class BatchPredictRequest(BaseModel):
    records: List[Dict[str, Any]] = Field(..., description="List of records.")

class BatchPredictResponse(BaseModel):
    predictions: List[float]
    model_version: str

class ErrorResponse(BaseModel):
    error: str
    model_version: Optional[str] = None
