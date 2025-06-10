FROM python:3.9

WORKDIR /workspace

COPY ./app/src /workspace
COPY ./app/requirements.txt /workspace

RUN mkdir -p /workspace/model
COPY ./model/model.pkl /workspace/model
COPY ./model/scaler.pkl /workspace/model

ENV MODEL_PATH=/workspace/model/model.pkl
ENV SCALER_PATH=/workspace/model/scaler.pkl

EXPOSE 30000

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "uvicorn", "main:app" ]
CMD [ "--host", "0.0.0.0", "--port", "30000" ]
