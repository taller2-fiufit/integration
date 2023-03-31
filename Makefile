install:
	poetry install

lint:
	poetry run flake8 fastapi_backend

mypy:
	poetry run mypy --strict .

test:
	poetry run pytest .
