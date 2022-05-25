from random import randint
from time import sleep

import requests
from opentelemetry import trace
# from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.http.trace_exporter import \
    OTLPSpanExporter
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Used by requests library
RequestsInstrumentor().instrument()

resource = Resource(attributes={"service.name": "fastapi_server_polling_service"})

trace.set_tracer_provider(TracerProvider(resource=resource))
endpoint = "http://agent:4318/v1/traces"

otlp_exporter = OTLPSpanExporter(endpoint=endpoint)
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)
tracer = trace.get_tracer(__name__)


def poll_fastapi_server():
    all_traces = 0
    traces_sampled = 0
    latency_sampled_traces = 0
    error_span_sampled_traces = 0

    while True:
        with tracer.start_as_current_span("send_request_to_server") as span:
            number1 = randint(1, 100)
            number2 = randint(0, 3)


            span.set_attribute("number1", number1)
            span.set_attribute("number2", number2)

            url = f"http://fastapi_server/divide/?number1={number1}&number2={number2}"

            response = requests.get(url)

            # Compute stats
            all_traces += 1
            if number2 == 0:
                error_span_sampled_traces += 1
                traces_sampled += 1
            elif number2 == 1:
                latency_sampled_traces += 1
                traces_sampled += 1
            print(f"Trace Sampling Stats as of now: All Traces: {all_traces} Sampled Traces: {traces_sampled} Latency sampled traces: {latency_sampled_traces} Error Span Sampled Traces: {error_span_sampled_traces}")


        sleep(2)


if __name__ == "__main__":
    poll_fastapi_server()
