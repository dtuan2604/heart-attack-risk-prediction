import requests
import os
import random
import logging
import uuid
import time

API_URL = os.getenv("API_URL", "http://localhost:8000")
SLEEP_INTERVAL = int(os.getenv("SLEEP_INTERVAL", 5))


def generate_good_request() -> dict:
    return {
        "age": random.randint(1, 100),
        "sex": random.choice(["male", "female"]),
        "total_cholesterol": random.uniform(80, 300),
        "ldl_cholesterol": random.uniform(30, 250),
        "hdl_cholesterol": random.uniform(20, 100),
        "systolic_bp": random.uniform(70, 200),
        "diastolic_bp": random.uniform(40, 120),
        "is_smoker": random.choice([True, False]),
        "diabetes": random.choice([True, False]),
    }


def generate_bad_request() -> dict:
    bad_request = generate_good_request()
    variations = [
        ("sex", random.randint(1, 100)),
        ("hdl_cholesterol", "high"),
        ("is_smoker", "smoking"),
        ("age", "twenty-five"),
    ]

    key, invalidValue = random.choice(variations)
    bad_request[key] = invalidValue

    return bad_request


def main():
    # Call the API
    while True:
        # 20% chance of a bad request
        request = generate_good_request()
        if random.random() < 0.2:
            request = generate_bad_request()

        request_id = uuid.uuid4()
        logging.info(f"Sending request: {request} with ID: {request_id}")

        headers = {"Content-Type": "application/json", "Request-ID": str(request_id)}

        try:
            response = requests.post(API_URL, json=request, headers=headers)
            logging.info(
                f"Request ID {request_id} got {response.status_code} return code. Response body: {response.text}"
            )
        except requests.exceptions.RequestException as e:
            logging.error(f"Can't connect to API: {e}")
            return

        time.sleep(SLEEP_INTERVAL)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
