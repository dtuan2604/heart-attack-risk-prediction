from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv, find_dotenv
from utility.model_utils import load_model, preprocess_input

import dto
import os
from loguru import logger

env_path = find_dotenv()
load_dotenv(env_path)

model_path = "".join([os.path.dirname(env_path), "/", os.getenv("MODEL_PATH")])
scaler_path = "".join([os.path.dirname(env_path), "/", os.getenv("SCALER_PATH")])
model = load_model(model_path)
scaler = load_model(scaler_path)

if model is None:
    raise RuntimeError(f"Model could not be loaded from {model_path}")


app = FastAPI()


@app.get("/", include_in_schema=False)
def get_doc():
    return RedirectResponse(url="/docs")


@app.get("/health")
def get_health():
    return {"status": "healthy"}


@app.post("/predict", response_model=dto.PredictionResponse)
def predict(patient_record: dto.PatientRecordDTO):
    """
    Predict the risk level and score for a given patient record.

    Args:
        patient_record (PatientRecordDTO): The patient record data.

    Returns:
        PredictionResponse: The prediction result containing risk level and score.
    """
    logger.info("Received patient record for prediction: {}", patient_record)

    # Convert DTO to model input format
    model_input = preprocess_input(scaler, patient_record)

    # Perform prediction
    prediction = model.predict_proba(model_input)[:, 1][0]

    # Create response
    response = dto.PredictionResponse(
        risk_level="low_risk"
        if prediction < 0.33
        else "medium_risk"
        if prediction < 0.66
        else "high_risk",
        risk_score=round(prediction * 100.0, 2),
    )

    logger.info("Prediction result: {}", response)

    return response
