.DEFAULT_GOAL := help

.PHONY: run-api-local help

# Dev commands
run-api-local:
	@echo "Running API locally..."
	cd app/src && uvicorn main:app --host 0.0.0.0 --port 8081

dev-unit-test:
	@echo "Running unit tests..."
	PYTHONPATH=app/src pytest --cache-clear

help:
	@echo "Makefile commands:"
	@echo "\t make run-api-local\t\t- Run the API locally"
