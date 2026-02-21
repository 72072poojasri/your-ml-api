from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List
import logging
import os
from src.model import load_model, preprocess_image, predict_image

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    load_model()
    logger.info("Model loaded successfully")

class PredictionResponse(BaseModel):
    class_label: str
    probabilities: List[float]

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict", response_model=PredictionResponse)
async def predict(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file type")

    image_bytes = await file.read()
    processed = preprocess_image(image_bytes)
    result = predict_image(processed)

    return result