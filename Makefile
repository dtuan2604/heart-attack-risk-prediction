.DEFAULT_GOAL := help

.PHONY: run-api-local help

#------------------Dev Commands------------------#
run-api-local:
	@echo "Running API locally..."
	cd app/src && uvicorn main:app --host 0.0.0.0 --port 8081

dev-unit-test:
	@echo "Running unit tests..."
	PYTHONPATH=app/src pytest --cache-clear

clean-up-python-cache:
	@echo "Cleaning up Python cache..."
	find . -type d \( -name ".pytest_cache" -o -name "__pycache__" \) -exec rm -rvf {} +

#------------------Dev Commands------------------#

help:
	@echo "Makefile commands:"
	@echo "\t make run-api-local\t\t- Run the API locally"
