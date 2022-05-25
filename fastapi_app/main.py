from typing import Union

from fastapi import FastAPI
from opentelemetry import trace

# from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor  # type:ignore

app = FastAPI()
FastAPIInstrumentor.instrument_app(app)


# Resource can be required for some backends, e.g. Jaeger
# If resource wouldn't be set - traces wouldn't appears in Jaeger
resource = Resource(attributes={"service.name": "fastapi_server"})

trace.set_tracer_provider(TracerProvider(resource=resource))
endpoint = "http://agent:4318/v1/traces"

otlp_exporter = OTLPSpanExporter(endpoint=endpoint)
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)
tracer = trace.get_tracer(__name__)


@app.get("/")
def index():
    with tracer.start_as_current_span("foo") as span:
        print(span.get_span_context())
        print(span.parent.trace_id)
        print(span.get_span_context().trace_id)
        print("Hello world!")
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
