from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

packages = find_packages()
package_data = {}


setup(
    name='llm-eval',
    version='0.1.0', # NOTE(chengmo): 修改此版本号时，请注意同时修改 __init__.py 中的 __version__
    author='yinjiaqi',
    author_email='1006272072@qq.com',
    packages=packages,
    package_data=package_data,
    install_requires=requirements,
    python_requires='>=3.9',
    extras_require={
        'serve': ['arize-phoenix==4.5.0']
    },
    entry_points={
        "console_scripts": [
            "phoenix_trace_server=llm_eval.trace.tracer.phoenix_trace:runtime_main",
        ]
    },
    description='LLM跟踪评估脚本'
)
