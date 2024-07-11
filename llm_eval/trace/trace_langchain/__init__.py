import time
from typing import Optional


from openinference.instrumentation.langchain import LangChainInstrumentor
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import (
    SpanExporter,
    SimpleSpanProcessor,
    ConsoleSpanExporter
) 

class LocalSpanExporter(SpanExporter):
    def __init__(self):
        self.spans = []

    def export(self, span_data):
        for span in span_data:
            self.spans.append(span)


def langchain_tracer(
    trace_phoenix: bool = True,
    trace_console: bool = False,
    local_span: Optional[LocalSpanExporter] = None
):
    resource = Resource(attributes={
    "service.name": "langchain"
    })  

    tracer_provider = TracerProvider(resource=resource)

    if trace_phoenix: # 将trace数据在本地可视化界面展示
        endpoint = "http://127.0.0.1:6006/v1/traces"
        tracer_provider.add_span_processor(SimpleSpanProcessor(OTLPSpanExporter(endpoint)))
    
    if trace_console: # 将trace数据在控制台展示
        tracer_provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))

    if local_span:
        tracer_provider.add_span_processor(SimpleSpanProcessor(local_span))

    trace.set_tracer_provider(tracer_provider)

    # 启动langcain的instrumentor打桩器
    LangChainInstrumentor().instrument()
    
    
    