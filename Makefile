install:
	python3 -m pip install --upgrade pip
	python3 -m venv pass-emploi-analytics-venv
	. pass-emploi-analytics-venv/bin/activate
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	pre-commit install
start:
	$(MAKE) install
	python3 main.py

