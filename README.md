# LLM-EVAL文档

## LLM-Trace 部分

### Trace LangChain

#### 启动phoenix可视化界面

```bash
phoenix_trace_server
```

- 默认phoenix常驻，使用ctrl+c退出结束程序

#### 设置环境变量与启动langchain跟踪器

```python
from llm_eval import langchain_tracer, LocalSpanExporter

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


#### 运行你的langchain文件
 
```python
# 配置并运行你的langchain文件
```

#### 导出本地容器储存的跟踪信息

```python
# 取出跟踪道德span信息列表
spans = local_span.spans

# print展示
for span in spans:
    print(span)
```

