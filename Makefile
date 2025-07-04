.DEFAULT_GOAL := help

.PHONY: run-api-local help

# ------------------Start Configuration------------------#
JENKIN_COMPOSE_FILE := jenkin/docker-compose-jenkin.yml
CLUSTER_POLICY_DIR := cluster-policy/

# ------------------End Configuration------------------#

#

#------------------Start Dev Commands------------------#
run-api-local:
	@echo "Running API locally..."
	set -a && source .env && set +a && \
	cd app/src && uvicorn main:app --host 0.0.0.0 --port 8082

dev-unit-test:
	@echo "Running unit tests..."
	PYTHONPATH=app/src \
	DISABLE_TRACING=true \
	DISABLE_METRICS=true \
	pytest --cache-clear

clean-up-python-cache:
	@echo "Cleaning up Python cache..."
	find . -type d \( -name ".pytest_cache" -o -name "__pycache__" \) -exec rm -rvf {} +

run-local-jenkin-docker:
	@echo "Running Jenkins Docker image..."
	docker compose -f docker-compose-jenkin.yml up --build -d && \
	docker exec -u 0 -it ci-cd-pipeline /bin/bash -c \
	"apt update > /dev/null 2>&1 && \
	apt install -y dnsutils > /dev/null 2>&1 && \
	IP=\$$(dig +short A host.docker.internal) && \
	[ -n \"\$$IP\" ] && echo \"\$$IP minikube\" >> /etc/hosts &&\
	chgrp docker /var/run/docker.sock"

run-local-jaeger:
	@echo "Running Jaeger Docker image..."
	docker compose -f docker-compose-jaeger.yml up --build -d

# I am using MacOS M1, so that I need to use the `--platform` flag to build for Linux
push-jenkin-image:
	@echo "Building and pushing Jenkins Docker image with multi architecture option to Docker Hub..."
	docker buildx build --platform linux/amd64,linux/arm64 -t tysonhoang/jenkin-with-cloud-plugin:latest --push jenkin

deploy-helm-locally:
	@echo "Deploying Helm chart locally..."
	helm upgrade --install hara helm-charts/hara --namespace model-serving

#------------------End Dev Commands------------------#
#------------------Start Cluster Command------------------#
update-cluster-policy:
	@echo "Updating cluster policy..."
	kubectl apply -k $(CLUSTER_POLICY_DIR)

get-jenkin-deployer-token:
	@echo "Getting Jenkins deployer token..."
	kubectl create token jenkins-deployer -n model-serving

start-nginx-system:
	@echo "Starting Nginx system in cluster..."
	helm upgrade --install nginx-ingress helm-charts/nginx-ingress --namespace nginx-system


#------------------End Cluster Command------------------#


help:
	@echo "Makefile commands:"
	@echo "\t make run-api-local\t\t- Run the API locally"
	@echo "\t make dev-unit-test\t\t- Run unit tests"
	@echo "\t make clean-up-python-cache\t- Clean up Python cache"
	@echo "\t make run-local-jenkin-docker\t- Run Jenkins in Docker locally"
	@echo "\t make push-jenkin-image\t\t- Build and push Jenkins Docker image to Docker Hub"
	@echo "\t make deploy-helm-locally\t- Deploy Helm chart locally"
	@echo "\t make update-cluster-policy\t- Update cluster policy"
	@echo "\t make get-jenkin-deployer-token\t- Get Jenkins deployer token"
	@echo "\t make start-nginx-system\t- Start Nginx system in cluster"
