.PHONY: venv run

venv:
	if not exist .venv uv venv

run: venv
	.venv\Scripts\activate && python main.py

exec: venv
	.venv\Scripts\activate && pyinstaller main.spec
