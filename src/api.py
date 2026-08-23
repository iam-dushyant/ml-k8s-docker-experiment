from pathlib import Path
import json
import logging
import os
import time

import joblib
from fastapi import FastAPI, Request
from fastapi.responses import Response
from pydantic import BaseModel, Field
from pythonjsonlogger.json import JsonFormatter
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST


# --- Logging configuration ---
handler = logging.StreamHandler()

handler.setFormatter(
    JsonFormatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s"
    )
)

logger = logging.getLogger("iris_api")
logger.handlers.clear()
logger.addHandler(handler)
logger.setLevel(logging.INFO)


# --- Load the trained model ---
MODEL_VERSION = os.getenv("MODEL_VERSION", "v2")

MODEL_DIR = Path("model") / MODEL_VERSION
MODEL_PATH = MODEL_DIR / "iris_rf.joblib"
META_PATH = MODEL_DIR / "metadata.json"

model = joblib.load(MODEL_PATH)

metadata = json.loads(
    META_PATH.read_text()
)

# --- Prometheus metrics configuration ---
REQUESTS = Counter(
    "iris_api_requests_total",
    "Total HTTP requests",
    ["method", "path", "status"],
    )

LATENCY = Histogram(
    "iris_api_request_latency_seconds",
    "HTTP request latency in seconds",
    ["method", "path"],
    )

PREDICTIONS = Counter(
    "iris_api_predictions_total",
    "Predictions by class",
    ["class_id", "model_version"],
    )

# --- FastAPI application ---
app = FastAPI(
    title="Iris ML Inference API",
    description="A simple API for predicting Iris flower species using a trained Random Forest model.",
    version=MODEL_VERSION,
)

# --- Request middleware for Prometheus metrics ---
@app.middleware("http")
async def add_metrics(request: Request, call_next):
    start = time.perf_counter()

    response = await call_next(request)

    duration_seconds = time.perf_counter() - start

    REQUESTS.labels(
        method=request.method,
        path=request.url.path,
        status=str(response.status_code),
    ).inc()

    LATENCY.labels(
        method=request.method,
        path=request.url.path,
    ).observe(duration_seconds)

    logger.info(
        "request_completed",
        extra={
            "method": request.method,
            "path": request.url.path,
            "status": response.status_code,
            "duration_ms": round(duration_seconds*1000, 2),
            "model_version": MODEL_VERSION,
        },
    )

    return response

# --- Request schema ---
class IrisFeatures(BaseModel):
    sepal_length: float = Field(gt=0)
    sepal_width: float = Field(gt=0)
    petal_length: float = Field(gt=0)
    petal_width: float = Field(gt=0)

# --- Routes ---
@app.get("/")
def root():
    return {
        "service": "Iris ML Inference API",
        "status": "running",
        "docs": "/docs",
        "health": "/health",
        "model": "/model",
    }


@app.get("/health")
def health():
    return {"status": "Okay"}


@app.post("/predict")
def predict(features: IrisFeatures):
    x = [[
        features.sepal_length,
        features.sepal_width,
        features.petal_length,
        features.petal_width,
    ]]

    prediction = int(model.predict(x)[0])
    probabilities = model.predict_proba(x)[0].tolist()

    logger.info(
        "prediction_completed",
        extra={
            "model_version": MODEL_VERSION,
            "class_id": prediction,
        },
    )

    return {
        "class_id": prediction,
        "probabilities": probabilities,
        "model_version": MODEL_VERSION,
    }


@app.get("/model")
def model_info():
    return metadata

@app.get("/metrics")
def metrics():
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )