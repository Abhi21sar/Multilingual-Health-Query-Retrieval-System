.PHONY: run test lint migrate

run:
	export PYTHONPATH=$PYTHONPATH:. && python3 app/api/main.py

test:
	export PYTHONPATH=$PYTHONPATH:. && python3 -m pytest tests/ -v

lint:
	ruff check . --fix

migrate:
	export PYTHONPATH=$PYTHONPATH:. && python3 app/scripts/migrate_data.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
