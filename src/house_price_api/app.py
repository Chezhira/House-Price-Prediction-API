import logging
import pandas as pd
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from .config import settings
from .logging_config import setup_logging
from .model_io import load_artifacts
from .features import add_features, align_columns, sanitize_cat_cols, sanitize_numeric_cols
from .schemas import PredictRequest, PredictResponse, BatchPredictRequest, BatchPredictResponse, ErrorResponse

setup_logging(settings.log_level)
log = logging.getLogger("house_price_api")

app = FastAPI(
    title="House Price Predictor (CatBoost)",
    version="1.0.0",
    description="Production-grade API for house price prediction using CatBoost and versioned artifacts.",
)

@app.get("/health")
def health():
    load_artifacts()
    return {"status": "ok", "model_version": settings.model_version}

def _predict_from_records(records: list[dict]) -> list[float]:
    model, feature_columns, cat_cols = load_artifacts()

    df = pd.DataFrame(records)
    df = add_features(df)

    X = align_columns(df, feature_columns)
    X = sanitize_cat_cols(X, cat_cols)
    X = sanitize_numeric_cols(X, cat_cols)

    preds = model.predict(X)
    return [float(p) for p in preds]

@app.post("/predict", response_model=PredictResponse, responses={400: {"model": ErrorResponse}})
def predict(req: PredictRequest):
    try:
        pred = _predict_from_records([req.record])[0]
        return PredictResponse(prediction=pred, model_version=settings.model_version)
    except Exception as e:
        log.exception("Prediction failed")
        return JSONResponse(
            status_code=400,
            content=ErrorResponse(error=str(e), model_version=settings.model_version).model_dump()
        )

@app.post("/predict_batch", response_model=BatchPredictResponse, responses={400: {"model": ErrorResponse}})
def predict_batch(req: BatchPredictRequest):
    try:
        preds = _predict_from_records(req.records)
        return BatchPredictResponse(predictions=preds, model_version=settings.model_version)
    except Exception as e:
        log.exception("Batch prediction failed")
        return JSONResponse(
            status_code=400,
            content=ErrorResponse(error=str(e), model_version=settings.model_version).model_dump()
        )
