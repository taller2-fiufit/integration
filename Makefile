install:
	poetry install

lint:
	poetry run flake8 fastapi_backend

mypy:
	poetry run mypy --strict .

format:
	poetry run black .

test:
	poetry run pytest .
