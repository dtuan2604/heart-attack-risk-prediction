from src.utility import load_model, preprocess_input
from src.dto import PatientRecordDTO
import pytest
import numpy as np


def test_load_model_success(mocker):
    mock_model = mocker.Mock()
    mocker.patch("joblib.load", return_value=mock_model)

    model = load_model("fake_model_path.pkl")
    assert model == mock_model


def test_load_model_failure(mocker):
    mocker.patch("joblib.load", side_effect=Exception("Load failed"))

    with pytest.raises(
        RuntimeError, match="Model could not be loaded from fake_model_path.pkl"
    ):
        load_model("fake_model_path.pkl")


def test_preprocess_input():
    patient_record = PatientRecordDTO(
        age=45,
        sex="male",
        total_cholesterol=200.0,
        ldl_cholesterol=130.0,
        hdl_cholesterol=50.0,
        systolic_bp=120.0,
        diastolic_bp=80.0,
        is_smoker=True,
        diabetes=False,
    )

    actual_output = preprocess_input(patient_record)

    assert isinstance(actual_output, np.ndarray)
    assert actual_output.shape == (1, 9)

    expected = [
        45.0,  # age
        1.0,  # sex (male)
        200.0,  # total_cholesterol
        130.0,  # ldl_cholesterol
        50.0,  # hdl_cholesterol
        120.0,  # systolic_bp
        80.0,  # diastolic_bp
        1.0,  # is_smoker
        0.0,  # diabetes
    ]

    np.testing.assert_allclose(actual_output[0], expected, rtol=1e-5)
