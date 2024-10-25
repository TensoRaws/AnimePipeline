.DEFAULT_GOAL := default

.PHONY: test
test:
	poetry run pytest --cov=animepipeline --cov-report=xml --cov-report=html

.PHONY: lint
lint:
	poetry run pre-commit install
	poetry run pre-commit run --all-files

.PHONY: build
build:
	poetry build --format wheel

.PHONY: run
run:
	poetry run python -m animepipeline

.PHONY: docker
docker:
	docker buildx build -t lychee0/animepipeline .
