.DEFAULT_GOAL := help

.PHONY: run-api-local help

# ------------------Start Configuration------------------#
JENKIN_COMPOSE_FILE := jenkin/docker-compose-jenkin.yml

# ------------------End Configuration------------------#

#

#------------------Start Dev Commands------------------#
run-api-local:
	@echo "Running API locally..."
	cd app/src && uvicorn main:app --host 0.0.0.0 --port 8081

dev-unit-test:
	@echo "Running unit tests..."
	PYTHONPATH=app/src pytest --cache-clear

clean-up-python-cache:
	@echo "Cleaning up Python cache..."
	find . -type d \( -name ".pytest_cache" -o -name "__pycache__" \) -exec rm -rvf {} +

run-local-jenkin-docker:
	@echo "Building Jenkins Docker image..."
# docker compose -f ${JENKIN_COMPOSE_FILE} up --build -d && docker exec -u 0 -it jenkins /bin/bash -c "apt update > /dev/null 2>&1 && apt install -y dnsutils > /dev/null 2>&1 && echo `dig +short A host.docker.internal` minikube >> /etc/hosts"
	docker compose -f jenkin/docker-compose-jenkin.yml up --build -d && \
	docker exec -u 0 -it jenkins /bin/bash -c \
	"apt update > /dev/null 2>&1 && \
	apt install -y dnsutils > /dev/null 2>&1 && \
	IP=\$$(dig +short A host.docker.internal) && \
	[ -n \"\$$IP\" ] && echo \"\$$IP minikube\" >> /etc/hosts"

# I am using MacOS M1, so I need to use the `--platform` flag to build for Linux
push-jenkin-image:
	@echo "Building and pushing Jenkins Docker image with multi architecture option to Docker Hub..."
	docker buildx build --platform linux/amd64,linux/arm64 -t tysonhoang/jenkin-with-cloud-plugin:latest --push jenkin

#------------------End Dev Commands------------------#
#------------------Start Cluster Command------------------#
update-cluster-policy:
	@echo "Updating cluster policy..."
	kubectl apply -k cluster-policy/
# kubectl create token jenkins-deployer -n model-serving


#------------------End Cluster Command------------------#


help:
	@echo "Makefile commands:"
	@echo "\t make run-api-local\t\t- Run the API locally"
