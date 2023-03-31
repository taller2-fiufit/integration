install:
	poetry install

lint:
	poetry run flake8

mypy:
	poetry run mypy --strict .

test:
	poetry run pytest .
