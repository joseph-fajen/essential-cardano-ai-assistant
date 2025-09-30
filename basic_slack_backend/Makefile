# Makefile
.PHONY: install run-local build deploy test clean auth-docker

# Project variables - UPDATE THESE BEFORE DEPLOYING
PROJECT_ID ?= essential-cardano-ai-assistant
REGION ?= us-central1
SERVICE_NAME ?= cardano-ai-slack-bridge
IMAGE_NAME = gcr.io/$(PROJECT_ID)/$(SERVICE_NAME)
REPO_NAME = basic_slack_backend
IMAGE = $(REGION)-docker.pkg.dev/$(PROJECT_ID)/$(REPO_NAME)/$(SERVICE_NAME)
SERVICE_ACCOUNT ?= cardano-ai-slack-service@$(PROJECT_ID).iam.gserviceaccount.com

# Install dependencies locally
install:
	uv venv
	uv pip install -e .

# Run locally with uv
run-local:
	uv run uvicorn main:app --reload --port 8000

# Run with environment variables
run-env:
	uv run --env-file .env uvicorn main:app --reload --port 8080

# Build Docker image
build:
	docker build -t $(SERVICE_NAME) .
	docker tag $(SERVICE_NAME) $(IMAGE_NAME)

test-docker: build
	# Just use host.docker.internal directly
	docker run --rm -p 8080:8080 \
	-e LANGGRAPH_URL=http://host.docker.internal:2024 \
	--env-file .env \
	$(SERVICE_NAME)
	
# Authenticate Docker with GCR
auth-docker:
	gcloud auth configure-docker gcr.io

# Build Docker image with proper tag
build:
	docker build -t $(SERVICE_NAME) .
	docker tag $(SERVICE_NAME) $(IMAGE_NAME)

# Push to GCR (requires auth-docker)
push: auth-docker
	docker push $(IMAGE_NAME)

# Build, push, and deploy
deploy:
	docker build --platform linux/amd64 -t $(SERVICE_NAME) .
	docker tag $(SERVICE_NAME) $(IMAGE)
	docker push $(IMAGE)
	gcloud run deploy $(SERVICE_NAME) \
		--image $(IMAGE) \
		--region $(REGION) \
		--allow-unauthenticated \
		--memory 2Gi \
		--timeout 300 \
		--env-vars-file .env.yaml \
		--service-account $(SERVICE_ACCOUNT)

# One-time setup
setup:
	gcloud auth login
	gcloud config set project $(PROJECT_ID)
	gcloud auth configure-docker gcr.io
	gcloud auth configure-docker $(REGION)-docker.pkg.dev
	gcloud artifacts repositories create $(REPO_NAME) --repository-format=docker --location=$(REGION)


# Clean up
clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .uv/
	rm -rf .venv/