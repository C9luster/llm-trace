from typing import Optional

from ..base import LocalSpanExporter

from openinference.instrumentation.langchain import LangChainInstrumentor
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import (
    SimpleSpanProcessor,
    ConsoleSpanExporter
) 

def langchain_tracer(
    trace_phoenix: bool = True,
    trace_console: bool = False,
    local_span: Optional[LocalSpanExporter] = None
):
    """
    初始化OpenTelemetry追踪器，用于在langchain服务中收集跟踪数据。
    
    Args:
        trace_phoenix (bool, optional): 是否将trace数据在本地Phoenix UI中展示。默认为True。
        trace_console (bool, optional): 是否将trace数据在控制台展示。默认为False。
        local_span (Optional[LocalSpanExporter], optional): 自定义的span处理器，用于处理span数据。默认为None。
    
    Returns:
        None
    
    """
    resource = Resource(attributes={
    "service.name": "langchain"
    })  

    tracer_provider = TracerProvider(resource=resource)

    if trace_phoenix: # 将trace数据在本地可视化界面展示
        endpoint = "http://127.0.0.1:8080/v1/traces"
        tracer_provider.add_span_processor(SimpleSpanProcessor(OTLPSpanExporter(endpoint)))
    
    if trace_console: # 将trace数据在控制台展示
        tracer_provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))

    if local_span:
        tracer_provider.add_span_processor(SimpleSpanProcessor(local_span))

    trace.set_tracer_provider(tracer_provider)

    # 启动langcain的instrumentor打桩器
    LangChainInstrumentor().instrument()