from random import randint
from time import sleep
import requests

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import \
    OTLPSpanExporter
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor


RequestsInstrumentor().instrument()

resource = Resource(attributes={"service.name": "some_python_service"})

trace.set_tracer_provider(TracerProvider(resource=resource))
endpoint = "http://agent2:4318/v1/traces"

otlp_exporter = OTLPSpanExporter(endpoint=endpoint)
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)
tracer = trace.get_tracer(__name__)


def generate_self_trace():
    while True:
        with tracer.start_as_current_span("start_trace") as span:
            sleep(1) # add delay of 1s to simulate some computation
            number = randint(101, 200)

            if number > 150:
                sleep(3)

                number1 = randint(200, 300)
                number2 = randint(0, 1)


                span.set_attribute("number1", number1)
                span.set_attribute("number2", number2)

                url = f"http://fastapi_server/divide/?number1={number1}&number2={number2}"
                response = requests.get(url)


            # url = "https://www.google.com"
            # response = requests.get(url)

            span.set_attribute("number", number)
            span.set_attribute("foo", "bar")
            print(number)


if __name__ == "__main__":
    generate_self_trace()
