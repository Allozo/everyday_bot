TESTS = tests/


VENV ?= .venv
CODE = tests src


.PHONY: venv
venv:
ifeq ($(OS), Windows_NT)
	python -m pip install --upgrade pip
	python -m pip install poetry
	poetry install
else
	python3.10 -m pip install --upgrade pip
	python3.10 -m pip install poetry
	poetry install
endif


.PHONY: test
test: ## Runs pytest
	poetry run python -m pytest $(TESTS)


.PHONY: lint
lint: ## Lint code
	poetry run python -m flake8 --jobs 4 --statistics --show-source $(CODE)
	poetry run python -m pylint --jobs 4 --rcfile=setup.cfg $(CODE)
	poetry run python -m mypy $(CODE)
	poetry run python -m black --skip-string-normalization --check $(CODE)


.PHONY: format
format: ## Formats all files
	poetry run python -m isort $(CODE)
	poetry run python -m black --skip-string-normalization $(CODE)
	poetry run python -m autoflake --recursive --in-place --remove-all-unused-imports $(CODE)
	poetry run python -m unify --in-place --recursive $(CODE)


.PHONY: ci
ci:	lint test ## Lint code then run tests


.PHONY: check
check: test format lint ## Fast check and fix


.PHONY: up
up:
	poetry run python -m src.vk_bot.vk_bot