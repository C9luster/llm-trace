# linux系统快捷安装包shell脚本
python3 -m pip uninstall llm_eval -y
rm -rf dist
python3 -u setup.py bdist_wheel
python3 -m pip install dist/*.whl
rm -rf dist
rm -rf build
rm -rf llm_eval.egg-info
