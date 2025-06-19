from functools import wraps
from opentelemetry import trace
from loguru import logger
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
import os


tracer = None


def init_tracer(service_name: str):
    """
    Initialize the tracer with the given service name.
    This function should be called at the start of the application.
    """
    global tracer
    if tracer is None:
        trace.set_tracer_provider(
            TracerProvider(resource=Resource.create({SERVICE_NAME: service_name}))
        )

        # Configure OTLP exporter endpoint, default to localhost collector
        otlp_endpoint = os.getenv(
            "OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317"
        )

        otlp_exporter = OTLPSpanExporter(endpoint=otlp_endpoint)

        span_processor = BatchSpanProcessor(otlp_exporter)
        trace.get_tracer_provider().add_span_processor(span_processor)

        tracer = trace.get_tracer_provider().get_tracer(
            instrumenting_module_name="hara", instrumenting_library_version="1.0.0"
        )

        logger.info(f"Tracing initialized with OTLP exporter at {otlp_endpoint}")
    else:
        logger.warning("Tracer is already initialized. Re-initialization is ignored.")


def trace_span(span_name: str):
    """
    Decorator to trace the execution of a function with a given span name.
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if os.getenv("DISABLE_TRACING", "false").lower() == "true":
                logger.info("Tracing is disabled. Skipping span creation.")
                return await func(*args, **kwargs)

            with tracer.start_as_current_span(span_name) as span:
                return await func(*args, **kwargs)

        return wrapper

    return decorator
