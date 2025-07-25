

#################################################################################
#
# Makefile to build the project
#
#################################################################################

PROJECT_NAME = ainsdale-beach-etl
PYTHON_INTERPRETER = python
WD=$(shell pwd)
PYTHONPATH=${WD}
PYTHONPATH_TEST=${WD}/src
SHELL := /bin/bash
PROFILE = default
PIP:=pip

## Create python interpreter environment.
create-environment:
	@echo ">>> About to create environment: $(PROJECT_NAME)..."
	@echo ">>> check python3 version"
	( \
		$(PYTHON_INTERPRETER) --version; \
	)
	@echo ">>> Setting up venv."
	( \
	    $(PYTHON_INTERPRETER) -m venv venv; \
	)

# Define utility variable to help calling Python from the virtual environment
ACTIVATE_ENV := source venv/bin/activate

# Execute python related functionalities from within the project's environment
define execute_in_env
	$(ACTIVATE_ENV) && $1
endef

## Build the environment requirements
requirements: create-environment
	$(call execute_in_env, $(PIP) install -r ./requirements.txt)

################################################################################################################
# Set Up
## Install bandit
bandit:
	$(call execute_in_env, $(PIP) install bandit)

## Install black
black:
	$(call execute_in_env, $(PIP) install black)

## Install coverage
coverage:
	$(call execute_in_env, $(PIP) install pytest-cov)

## Set up dev requirements (bandit, black & coverage)
dev-setup: bandit black coverage

# Build / Run

## Run the security test (bandit)
security-test:
	$(call execute_in_env, bandit -lll */*.py *c/*/*.py)

## Run the black code check
run-black:
	$(call execute_in_env, black  ./src/*.py ./test/*.py)

## Run the unit tests
unit-test:
	$(call execute_in_env, PYTHONPATH=${PYTHONPATH_TEST} pytest -v)

## Run the coverage check
check-coverage:
	$(call execute_in_env, PYTHONPATH=${PYTHONPATH_TEST} pytest --cov=src test/)

## Run all checks
run-checks: security-test run-black unit-test check-coverage

run-all: requirements dev-setup run-checks