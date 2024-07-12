from opentelemetry.sdk.trace.export import SpanExporter

class LocalSpanExporter(SpanExporter):
    def __init__(self):
        self.spans = []

    def export(self, span_data):
        for span in span_data:
            self.spans.append(span)