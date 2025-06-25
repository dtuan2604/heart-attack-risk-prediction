FROM python:3.9-slim

WORKDIR /client-space

COPY ./test_client.py /client-space

RUN pip install --no-cache-dir requests

ENTRYPOINT [ "python", "test_client.py" ]
