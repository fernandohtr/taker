install-taker:
	pip install -r src/taker/requirements/base.txt

install-taker-dev:
	pip install -r src/taker/requirements/dev.txt

run-taker:
	python src/taker/run.py
