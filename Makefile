.PHONY: test api

test:
	poetry run pytest -v

api:
	poetry run python src/api/app.py
