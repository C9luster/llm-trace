# Trace 功能

## Trace LangChain

### 启动phoenix可视化界面

```bash
phoenix_trace_server
```

- 默认phoenix常驻，使用ctrl+c退出结束程序

### 设置环境变量与启动langchain跟踪器

```python
from llm_eval.trace import langchain_tracer, LocalSpanExporter

# 创建跟踪信息储存容器
local_span = LocalSpanExporter()

# 启动跟踪器
langchain_tracer(
    trace_phoenix = True,
    trace_console = True,
    local_span=local_span
    )
```
langchain_tracer()函数有四个参数
- race_phoenix: Optional[bool] = True
  - 是否向phoenix可视化界面传参，默认为True
- trace_console: Optional[bool] = True
  - 控制台输出跟踪信息，默认为False
- local_span: Optional[LocalSpanExporter] = None
  - 跟踪信息储存容器，非必填项，默认为空，则不进行变量储存


### 运行你的langchain文件
 
```python
# 配置并运行你的langchain框架
```

### 导出本地容器储存的跟踪信息

#### 导出并查看每个Span节点的信息(json格式)

- local_span.spans 的类型为list，储存的数据类型为ReadableSpan，答应出json格式的span信息

```python
# 取出跟踪道德span信息列表,输出的结果为一个迭代器
spans = local_span.span_json()

# 使用迭代器流式输出json格式的span信息
for span in spans:
    print(span)
```

#### 查看整个运行流程LLM的调用信息

- llms_message()函数返回的为一个，可流式查看LLM调用星系，且返回值为dict字典类型

```python
llm_message = local_span.llms_message()
for message in llm_message:
    print(message)
```