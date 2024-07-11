python3 -m pip uninstall llm_eval -y
rm -rf dist
python3 -u setup.py bdist_wheel
python3 -m pip install dist/*.whl
