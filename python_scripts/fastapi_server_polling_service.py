from random import randint
from time import sleep

import requests
from opentelemetry import trace
# from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.http.trace_exporter import \
    OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.urllib import URLLibInstrumentor  # type: ignore

# Used by requests library
URLLibInstrumentor().instrument()


resource = Resource(attributes={"service.name": "fastapi_server_polling_service"})

trace.set_tracer_provider(TracerProvider(resource=resource))
endpoint = "http://agent:4318/v1/traces"

otlp_exporter = OTLPSpanExporter(endpoint=endpoint)
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)
tracer = trace.get_tracer(__name__)


def poll_fastapi_server():
    while True:
        with tracer.start_as_current_span('send_request_to_server') as span:
            number1 = randint(1, 100)
            number2 = randint(0, 5)
            print(number1, number2)

            span.set_attribute("number1", number1)
            span.set_attribute("number2", number2)

            url = f"http://fastapi_server/divide/?number1={number1}&number2={number2}"

            response = requests.get(url)
            sleep(5)


if __name__ == "__main__":
    poll_fastapi_server()
