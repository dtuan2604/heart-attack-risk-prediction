run-api-local:
	@echo "Running API locally..."
	cd app/src && uvicorn main:app --host 0.0.0.0 --port 8081

help:
	@echo "Makefile commands:"
	@echo "\t make run-api-local\t\t- Run the API locally"