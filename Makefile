install:
	python3 -m venv .venv
	. .venv/bin/activate && pip install -r requirements.txt

run:
	python run.py

test:
	pytest

doctor:
	python check_install.py
