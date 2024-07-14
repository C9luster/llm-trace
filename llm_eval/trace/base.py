import json

from opentelemetry.sdk.trace.export import SpanExporter

class LocalSpanExporter(SpanExporter):
    _exporter = None

    def __new__(cls, *args, **kwargs):
        if cls._exporter is None:
            cls._exporter = super().__new__(cls)
        return cls._exporter

    def __init__(self):
        """
        初始化方法，创建一个空的文本片段列表（spans）和空的LLM文本片段列表（llm_spans）。
        
        Args:
            无。
        
        Returns:
            无返回值，初始化实例属性。
        
        """
        self.spans = []
        self.llms = []

    def export(self, span_data):
        """
        将span_data中的span添加到当前对象的spans列表中。
        
        Args:
            span_data (list): 包含多个span的列表，每个span应该是一个字典类型，包含span的相关信息。
        
        Returns:
            None: 此函数没有返回值，但会修改当前对象的spans列表。
        
        """
        for span in span_data:
            self.spans.append(span)

    def span_json(self):
        """
        将对象的spans列表中的每个span对象转换为JSON格式的字符串并生成器返回。
        
        Args:
            无。
        
        Returns:
            Generator[str, None, None]: 返回一个生成器，生成器中的每个元素是span对象转换为JSON格式的字符串。
        
        """
        for span in self.spans:
            yield span.to_json()

    def _llm_spans(self):
        """
        从span列表中筛选出类型为'llm'的span，并构建对应的字典存入llms列表中。
        
        Args:
            无。
        
        Returns:
            无返回值，但会修改对象的llms属性，将其更新为包含所有'llm'类型span信息的列表。
        
        """
        for span in self.spans:
            if hasattr(span, 'attributes') and span.attributes and span.attributes.get('openinference.span.kind', None):
                if span.attributes['openinference.span.kind'].lower() == 'llm':
                    llm_dict = {}
                    attributes = span.attributes
                    llm_dict['kind'] = attributes.get('openinference.span.kind', None)
                    llm_dict['model_name'] = attributes.get('llm.model_name', None)
                    input = attributes.get('input.value', None)
                    if input and isinstance(input, str):
                        input_dict = json.loads(input)
                        input = ''
                        for value in input_dict.values():
                            if isinstance(value, list):
                                for message in value:
                                    input = '{}{}'.format(input, message)+'\n'
                        if input.endswith('\n'):
                            input = input[:-1]
                        llm_dict['input'] = input
                    output = attributes.get('output.value', None)
                    if output and isinstance(output, str):
                        input_tokens = 0
                        output_tokens = 0
                        total_tokens = 0
                        output_dict = json.loads(output)
                        output = ''
                        for key, value in output_dict.items():
                            if key == 'generations':
                                 if isinstance(value, list):
                                    for message in value:
                                        if isinstance(message, list):
                                            for message_value in message:
                                                if isinstance(message_value, dict):
                                                    output = '{}{}'.format(output, message_value['text'])+'\n'
                                                    if message_value.get('generation_info', None) and message_value['generation_info'].get('token_usage', None):
                                                        input_tokens += message_value['generation_info']['token_usage'].get('input', 0)
                                                        output_tokens += message_value['generation_info']['token_usage'].get('output', 0)
                                                        total_tokens += message_value['generation_info']['token_usage'].get('total', 0)
                        if output.endswith('\n'):
                            output = output[:-1]
                        llm_dict['output'] = output  
                        llm_dict['input_tokens'] = input_tokens
                        llm_dict['output_tokens'] = output_tokens
                        llm_dict['total_tokens'] = total_tokens
                    self.llms.append(llm_dict)
                