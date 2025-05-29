from pydantic import BaseModel, Field


class PatientRecordDTO(BaseModel):
    age: int = Field(..., description="Age of the patient in years")
    sex: str = Field(
        ..., description="The bilogical sex of the patient", pattern="^(male|female)$"
    )
    total_cholesterol: float = Field(
        ..., description="Total cholesterol level in mg/dL"
    )
    ldl_cholesterol: float = Field(..., description="LDL cholesterol level in mg/dL")
    hdl_cholesterol: float = Field(..., description="HDL cholesterol level in mg/dL")
    systolic_bp: float = Field(..., description="Systolic blood pressure in mmHg")
    diastolic_bp: float = Field(..., description="Diastolic blood pressure in mmHg")
    is_smoker: bool = Field(..., description="Indicates if the patient is a smoker")
    diabetes: bool = Field(..., description="Indicates if the patient has diabetes")
