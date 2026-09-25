"""OpenTelemetry bootstrap; no-op compatible when collector is absent."""
from opentelemetry import trace
try:
 from opentelemetry.sdk.resources import Resource
 from opentelemetry.sdk.trace import TracerProvider
 from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
 provider=TracerProvider(resource=Resource.create({"service.name":"distributed-ai-inference-platform"}))
 provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
 trace.set_tracer_provider(provider)
except Exception:
 pass
tracer=trace.get_tracer("distributed-ai-inference-platform")
