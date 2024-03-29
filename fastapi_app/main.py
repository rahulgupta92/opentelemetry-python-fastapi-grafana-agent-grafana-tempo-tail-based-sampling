from time import sleep
from typing import Union

from fastapi import FastAPI, Request
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import \
    OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import \
    FastAPIInstrumentor  # type:ignore
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

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
    return {"Hello": "World"}


@app.get("/divide/")
def division(request: Request, number1: int, number2: int):
    print('---headers---', request.headers)
    with tracer.start_as_current_span("divide_numbers") as span:

        print(span.get_span_context())

        span.set_attribute("number1", number1)
        span.set_attribute("number2", number2)

        result = number1 / number2

        if number2 == 1:
            sleep(3)
        else:
            sleep(1) # add delay of 1s to simulate some computation

        span.set_attribute("result", result)

        if number2 == 3:
            span.set_attribute('dont_sample', 'yes')

    return {"result": result}
