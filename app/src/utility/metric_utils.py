from prometheus_client import start_http_server
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.metrics import set_meter_provider
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry import metrics
import os
from loguru import logger


def init_metrics(service_name: str, version: str, port: int):
    """
    Initialize an Opentelemetry metrics and starts the Prometheus exporter
    """
    if os.getenv("DISABLE_METRICS", "false").lower() == "true":
        logger.warning("Metric is disabled. Skipping metric initialization.")
        return None

    start_http_server(port=port, addr="0.0.0.0")

    resource = Resource(attributes={SERVICE_NAME: service_name})

    reader = PrometheusMetricReader()
    provider = MeterProvider(resource=resource, metric_readers=[reader])
    set_meter_provider(provider)

    logger.info(f"Start exposing Prometheus metric at port {port}")
    return metrics.get_meter(name=service_name, version=version)


meter = init_metrics(
    service_name=os.getenv("SERVICE_NAME", "hara-service"),
    version=os.getenv("APP_VERSION", "0.0.1"),
    port=int(os.getenv("METRIC_PORT", "8099")),
)

reqs_counter = (
    meter.create_counter(
        name="total_request_count", description="Total number of prediction requests"
    )
    if meter
    else None
)

latency_hist = (
    meter.create_histogram(
        name="request_latency_seconds",
        description="Historgram of prediction latency in seconds",
        unit="seconds",
    )
    if meter
    else None
)
