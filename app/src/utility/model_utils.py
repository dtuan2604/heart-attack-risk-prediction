from typing import Optional
from dto import PatientRecordDTO
from sklearn.preprocessing import StandardScaler
from loguru import logger
import numpy as np
from numpy.typing import NDArray
import joblib


def load_model(model_path: str) -> Optional[object]:
    """
    Load a machine learning model from a specified path. Return None if loading fails.

    Args:
        model_path (str): The file path to the model.

    Returns:
        The loaded model.
    """
    try:
        logger.info(f"Loading model from {model_path}")
        model = joblib.load(model_path)
        return model
    except Exception as e:
        logger.debug(f"Failed to load model from {model_path}: {e}")
        raise RuntimeError(f"Model could not be loaded from {model_path}") from e


def preprocess_input(
    scaler: StandardScaler, input_data: PatientRecordDTO
) -> NDArray[np.float64]:
    """
    Preprocess input data to ensure it matches the model's expected format.

    Args:
        input_data (dict): The input data to preprocess.

    Returns:
        dict: The preprocessed input data.
    """
    # Example preprocessing logic
    # This should be customized based on the model's requirements
    preprocessed_input = input_data.model_dump()
    logger.debug(f"Raw input data: {preprocessed_input}")

    # Convert categorical variables to numerical
    preprocessed_input["sex"] = 1 if preprocessed_input["sex"].lower() == "male" else 0
    preprocessed_input["is_smoker"] = 1 if preprocessed_input["is_smoker"] else 0
    preprocessed_input["diabetes"] = 1 if preprocessed_input["diabetes"] else 0

    # Convert int to float for consistency
    for key in preprocessed_input:
        if isinstance(preprocessed_input[key], int):
            preprocessed_input[key] = float(preprocessed_input[key])

    # Convert to numpy array
    preprocessed_array = np.array(list(preprocessed_input.values())).reshape(1, -1)

    # Standardize the data
    preprocessed_data = scaler.transform(preprocessed_array)

    return preprocessed_data
