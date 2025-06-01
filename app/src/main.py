from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, JSONResponse
from dotenv import load_dotenv, find_dotenv
from utility import load_model, preprocess_input
from dto import PatientRecordDTO, PredictionResponse
from loguru import logger
from fastapi.exceptions import RequestValidationError

import os


env_path = find_dotenv()
load_dotenv(env_path)

model_path = "".join([os.path.dirname(env_path), "/", os.getenv("MODEL_PATH")])
scaler_path = "".join([os.path.dirname(env_path), "/", os.getenv("SCALER_PATH")])
model = load_model(model_path)
scaler = load_model(scaler_path)

app = FastAPI()


@app.get("/", include_in_schema=False)
def get_doc() -> RedirectResponse:
    return RedirectResponse(url="/docs")


@app.get("/health")
def get_health() -> JSONResponse:
    return JSONResponse(
        status_code=200,
        content={"status": "healthy"},
    )


@app.post("/predict", response_model=PredictionResponse)
def predict(patient_record: PatientRecordDTO) -> JSONResponse:
    """
    Predict the risk level and score for a given patient record.

    Args:
        patient_record (PatientRecordDTO): The patient record data.

    Returns:
        PredictionResponse: The prediction result containing risk level and score.
    """
    logger.info("Received patient record for prediction: {}", patient_record)

    # Convert DTO to model input format
    preprocessed_input = preprocess_input(patient_record)

    # Standardize the input data
    model_input = scaler.transform(preprocessed_input)

    # Perform prediction
    prediction = model.predict_proba(model_input)[:, 1][0]

    # Create response
    response = PredictionResponse(
        risk_level="low_risk"
        if prediction < 0.33
        else "medium_risk"
        if prediction < 0.66
        else "high_risk",
        risk_score=round(prediction * 100.0, 2),
    )

    logger.info("Prediction result: {}", response)

    return response


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """
    Custom exception handler for request validation errors.
    """
    logger.error("Validation error: {}", exc)
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body},
    )
