import json

from opentelemetry.sdk.trace.export import SpanExporter

class LocalSpanExporter(SpanExporter):
    _exporter = None

    def __new__(cls, *args, **kwargs):
        """
        返回该类实例，若该类未创建过实例，则创建并返回该类的单例对象。
        
        Args:
            *args: 可变位置参数，传递给类的构造函数。
            **kwargs: 可变关键字参数，传递给类的构造函数。
        
        Returns:
            cls: 该类的单例对象。
        
        """
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
        self.retrievers = []
        self.agents = []
        self.llms_spanId = []
        self.retrievers_spanId = []
        self.agents_spanId = []

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
                if span.attributes['openinference.span.kind'].lower().startswith('llm'):
                    llm_dict = {}
                    attributes = span.attributes
                    llm_dict['kind'] = attributes.get('openinference.span.kind', None)
                    llm_dict['model_name'] = attributes.get('llm.model_name', None)
                    if hasattr(span, 'context') and span.context and hasattr(span.context, 'trace_id') and span.context.trace_id:
                            llm_dict['trace_id'] = span.context.trace_id
                    if hasattr(span, 'context') and span.context and hasattr(span.context, 'span_id') and span.context.span_id:
                        llm_dict['span_id'] = span.context.span_id
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
                                                        input_tokens += message_value['generation_info']['token_usage'].get('input_tokens', 0)
                                                        output_tokens += message_value['generation_info']['token_usage'].get('output_tokens', 0)
                                                        total_tokens += message_value['generation_info']['token_usage'].get('total_tokens', 0)
                        if output.endswith('\n'):
                            output = output[:-1]
                        llm_dict['output'] = output  
                        llm_dict['input_tokens'] = input_tokens
                        llm_dict['output_tokens'] = output_tokens
                        llm_dict['total_tokens'] = total_tokens
                    if llm_dict['span_id'] and llm_dict['span_id'] not in self.llms_spanId:
                        self.llms_spanId.append(llm_dict['span_id'])
                        self.llms.append(llm_dict)
        
    def _retriever_spans(self):
        """
        从给定的span列表中检索出类型为retriever的span，并返回对应的retriever字典列表。
        
        Args:
            无参数。
        
        Returns:
            List[Dict[str, Any]]: 包含类型为retriever的span的retriever字典列表。
        
        """

        for span in self.spans:
            if hasattr(span, 'attributes') and span.attributes and span.attributes.get('openinference.span.kind', None):
                if span.attributes['openinference.span.kind'].lower().startswith('retriever'):
                    retriever_dict = {}
                    attributes = span.attributes
                    retriever_dict['kind'] = attributes.get('openinference.span.kind', None)
                    if hasattr(span, 'context') and span.context and hasattr(span.context, 'trace_id') and span.context.trace_id:
                        retriever_dict['trace_id'] = span.context.trace_id
                    if hasattr(span, 'context') and span.context and hasattr(span.context, 'span_id') and span.context.span_id:
                        retriever_dict['span_id'] = span.context.span_id
                    retriever_dict['input'] = attributes.get('input.value', None)
                    output = attributes.get('output.value', None)
                    if output:
                        output_dict = json.loads(output)
                        documents = output_dict.get('documents', None)
                        if documents:
                            print(type(documents))
                            retriever_dict['output'] = documents
                    if retriever_dict['span_id'] and retriever_dict['span_id'] not in self.retrievers_spanId:
                        self.retrievers_spanId.append(retriever_dict['span_id'])
                        self.retrievers.append(retriever_dict)
    

    def _agent_spans(self):
        """
        从给定的span列表中检索出类型为agent的span，并返回对应的agent字典列表。
        
        Args:
            无参数。
        
        Returns:
            List[Dict[str, Any]]: 包含类型为agent的span的agent字典列表。
            
        """
        for span in self.spans:
            if hasattr(span, 'attributes') and span.attributes and span.attributes.get('openinference.span.kind', None):
                if span.attributes['openinference.span.kind'].lower().startswith('agent'):
                    attributes = span.attributes
                    agent_dict = {}
                    if hasattr(span, 'context') and span.context and hasattr(span.context, 'trace_id') and span.context.trace_id:
                        agent_dict['trace_id'] = span.context.trace_id
                    if hasattr(span, 'context') and span.context and hasattr(span.context, 'span_id') and span.context.span_id:
                        agent_dict['span_id'] = span.context.span_id
                    if attributes:
                        agent_dict['input'] = attributes.get('input.value', None)
                        agent_dict['output'] = attributes.get('output.value', None)
                    if agent_dict['span_id'] and agent_dict['span_id'] not in self.agents_spanId:
                        self.agents_spanId.append(agent_dict['span_id'])
                        self.agents.append(agent_dict)
                
    
    def llms_message(self):  
        """
        生成器函数，用于遍历并返回LLM消息列表。
        
        Args:
            无参数。
        
        Returns:
            生成器: 返回一个生成器，该生成器在每次迭代时都会生成一个LLM消息。
        
        """
        self._llm_spans()
        for llm_message in self.llms:
            yield llm_message

    def retriever_message(self):
        """
        返回Retriever对象的消息列表生成器。
        
        Args:
            无。
        
        Returns:
            生成器: 包含Retriever对象消息的生成器。
        
        """
        self._retriever_spans()
        for retriever_message in self.retrievers:
            yield retriever_message

    def agent_message(self):
        """
        返回Agent对象的消息列表生成器。
        Args:
            无。
        Returns:
            生成器: 包含Agent对象消息的生成器。
        """
        self._agent_spans()
        for agent_message in self.agents:
            yield agent_message
                