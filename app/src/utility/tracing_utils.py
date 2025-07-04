from functools import wraps
from opentelemetry import trace
from loguru import logger
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
import os


def init_tracer(service_name: str, version: str, otlp_endpoint: str):
    """
    Initialize the tracer with the given service name.
    This function should be called at the start of the application.
    """
    if os.getenv("DISABLE_TRACING", "false").lower() == "true":
        logger.warning("Tracing is disabled. Skipping tracer initialization.")
        return None

    trace.set_tracer_provider(
        TracerProvider(resource=Resource.create({SERVICE_NAME: service_name}))
    )

    # Configure OTLP exporter endpoint, default to localhost collector

    otlp_exporter = OTLPSpanExporter(endpoint=otlp_endpoint, insecure=True)

    span_processor = BatchSpanProcessor(otlp_exporter)
    trace.get_tracer_provider().add_span_processor(span_processor)

    tracer = trace.get_tracer_provider().get_tracer(
        instrumenting_module_name=service_name, instrumenting_library_version=version
    )

    logger.info(f"Initialized connection with OTLP exporter at {otlp_endpoint}")
    return tracer


tracer = init_tracer(
    service_name=os.getenv("SERVICE_NAME", "hara-service"),
    version=os.getenv("APP_VERSION", "0.0.1"),
    otlp_endpoint=os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317"),
)


def trace_span(span_name: str):
    """
    Decorator to trace the execution of a function with a given span name.
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if not tracer:
                logger.info("Tracing is disabled. Skipping span creation.")
                return await func(*args, **kwargs)

            with tracer.start_as_current_span(span_name) as span:
                return await func(*args, **kwargs)

        return wrapper

    return decorator
