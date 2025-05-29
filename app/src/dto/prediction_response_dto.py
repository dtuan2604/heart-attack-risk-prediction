from pydantic import BaseModel, Field


class PredictionResponse(BaseModel):
    risk_level: str = Field(
        ...,
        description="The risk level of the patient based on the prediction model",
        pattern="^(low_risk|medium_risk|high_risk)$",
    )
    risk_score: float = Field(
        ...,
        description="The numerical risk score assigned to the patient",
        ge=0.0,
        le=100.0,
    )
