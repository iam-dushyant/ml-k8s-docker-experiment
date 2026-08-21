from pathlib import Path
import joblib
from fastapi import FastAPI
from pydantic import BaseModel, Field

MODEL_PATH = Path("model/iris_rf.joblib")
model = joblib.load(MODEL_PATH)

app = FastAPI(title="Iris Classifier API", version="1.0.0")

class IrisFeatures(BaseModel):
    sepal_length: float = Field(gt=0)
    sepal_width: float = Field(gt=0)
    petal_length: float = Field(gt=0)
    petal_width: float = Field(gt=0)

@app.get("/")
def root():
    return {
        "service": "Iris ML Inference API",
        "status": "running",
        "docs": "/docs",
        "health": "/health"
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
        features.petal_width
    ]]

    prediction = int(model.predict(x)[0])
    probabilities = model.predict_proba(x)[0].tolist()
    return {"class_id":prediction, "probabilities": probabilities}