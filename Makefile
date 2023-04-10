install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

source_code:
	python get_data.py && python get_data_stats.py

test:
	python -m pytest -vv --cov get_data --cov get_data_stats test_data_checks.py

all: install test
