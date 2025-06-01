from src import app
from src.dto import PatientRecordDTO
from fastapi.testclient import TestClient
import pytest
import numpy as np
import json
from typing import List


client = TestClient(app)


def generate_random_patient_record() -> PatientRecordDTO:
    """Generate a random patient record for testing."""
    import random

    return PatientRecordDTO(
        age=random.randint(18, 90),
        sex=random.choice(["male", "female"]),
        total_cholesterol=round(random.uniform(150, 300), 1),
        ldl_cholesterol=round(random.uniform(80, 200), 1),
        hdl_cholesterol=round(random.uniform(30, 100), 1),
        systolic_bp=round(random.uniform(90, 180), 1),
        diastolic_bp=round(random.uniform(60, 110), 1),
        is_smoker=random.choice([True, False]),
        diabetes=random.choice([True, False]),
    )


def good_patient_record() -> List[tuple]:
    """Generate a list of good patient records for testing."""
    expected_risk_level = ["low_risk", "medium_risk", "high_risk"]
    expected_risk_score = [0.3, 0.5, 0.8]
    return [
        (
            expected_risk_level[i],
            expected_risk_score[i],
            generate_random_patient_record().model_dump_json(),
        )
        for i in range(len(expected_risk_level))
    ]


def bad_patient_record() -> dict:
    """Generate a list of bad patient records for testing."""
    test_cases = ["missing", "bool_parsing", "string_pattern_mismatch"]
    test_data = {
        case: generate_random_patient_record().model_dump() for case in test_cases
    }

    # Missing fields
    del test_data["missing"]["age"]

    # Invalid data type
    test_data["bool_parsing"]["is_smoker"] = "123"

    # Fail regex
    test_data["string_pattern_mismatch"]["sex"] = "unknown"

    return [(key, json.dumps(test_data[key])) for key in test_data]


@pytest.fixture(params=good_patient_record())
def mock_model_and_scaler_for_good_patient_record(mocker, request):
    mock_risk_level, mock_risk_score, patient_record = request.param

    mocked_scaler = mocker.Mock()
    mocked_model = mocker.Mock()

    mocked_scaler.transform.return_value = np.random.rand(1, 9)
    mocked_model.predict_proba.return_value = np.array(
        [[1 - mock_risk_score, mock_risk_score]]
    )

    mocker.patch("src.main.model", mocked_model)
    mocker.patch("src.main.scaler", mocked_scaler)

    return (
        mocked_model,
        mocked_scaler,
        mock_risk_level,
        round(mock_risk_score * 100, 2),
        patient_record,
    )


@pytest.fixture(params=bad_patient_record())
def mock_model_and_scaler_for_bad_patient_record(mocker, request):
    mock_error, mock_request = request.param
    mocked_scaler = mocker.Mock()
    mocked_model = mocker.Mock()

    mocked_scaler.transform.return_value = np.random.rand(1, 9)
    mocked_model.predict_proba.return_value = np.array([[0.9, 0.1]])

    mocker.patch("src.main.model", mocked_model)
    mocker.patch("src.main.scaler", mocked_scaler)

    return (mocked_model, mocked_scaler, mock_error, mock_request)


def test_root():
    response = client.get("/")
    assert response.status_code == 200


def test_get_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_predict_endpoint_with_good_patient_record(
    mock_model_and_scaler_for_good_patient_record,
):
    (
        mocked_model,
        mocked_scaler,
        expected_risk_level,
        expected_risk_score,
        patient_record,
    ) = mock_model_and_scaler_for_good_patient_record
    response = client.post(
        "/predict", content=patient_record, headers={"Content-Type": "application/json"}
    )

    assert response.status_code == 200
    mocked_scaler.transform.assert_called_once()
    mocked_model.predict_proba.assert_called_once()
    assert response.json()["risk_level"] == expected_risk_level
    assert response.json()["risk_score"] == expected_risk_score


def test_predict_endpoint_with_bad_patient_record(
    mock_model_and_scaler_for_bad_patient_record,
):
    (
        mocked_model,
        mocked_scaler,
        expected_error,
        mock_request,
    ) = mock_model_and_scaler_for_bad_patient_record
    response = client.post(
        "/predict", content=mock_request, headers={"Content-Type": "application/json"}
    )

    assert response.status_code == 422  # Expecting validation error
    mocked_scaler.transform.assert_not_called()
    mocked_model.predict_proba.assert_not_called()

    response_json = response.json()
    print(response_json)
    assert response_json["detail"][0]["type"] == expected_error
