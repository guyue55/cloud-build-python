#!/bin/bash

# This script deploys the StoryCraft application to Google Cloud using gcloud commands.
# It mirrors the infrastructure defined in the Terraform configuration.

# --- Configuration ---
# Replace these variables with your actual project details.
PROJECT_ID=$(gcloud config get-value project)
REPOSITORY="cloud-service"
export PROJECT_ID=${PROJECT_ID}
export REGION="us-central1"

export SERVICE_ACCOUNT_NAME="ai-cloud-service"

# --- Script ---

# Set the project for all subsequent gcloud commands
gcloud config set project $PROJECT_ID

# 1. Enable required APIs
echo "Enabling required Google Cloud APIs..."
gcloud services enable \
  run.googleapis.com \
  cloudbuild.googleapis.com \
  containerregistry.googleapis.com \
  artifactregistry.googleapis.com \
  aiplatform.googleapis.com \
  iam.googleapis.com \
  cloudresourcemanager.googleapis.com

# 2. Create Service Account
export SERVICE_ACCOUNT_EMAIL="${SERVICE_ACCOUNT_NAME}@$PROJECT_ID.iam.gserviceaccount.com"

echo "Creating service account: $SERVICE_ACCOUNT_NAME..."
if ! gcloud iam service-accounts describe $SERVICE_ACCOUNT_EMAIL > /dev/null 2>&1; then
    gcloud iam service-accounts create $SERVICE_ACCOUNT_NAME \
    --display-name="AI App V3 Service Account" \
    --description="Service account for Cloud Build Python AI application"
else
    echo "Service account $SERVICE_ACCOUNT_NAME already exists."
fi

# 3. Grant IAM roles to the service account
echo "Granting IAM roles to the service account..."
gcloud projects add-iam-policy-binding $PROJECT_ID --member="serviceAccount:$SERVICE_ACCOUNT_EMAIL" --role="roles/aiplatform.user"
gcloud projects add-iam-policy-binding $PROJECT_ID --member="serviceAccount:$SERVICE_ACCOUNT_EMAIL" --role="roles/logging.logWriter"
gcloud projects add-iam-policy-binding $PROJECT_ID --member="serviceAccount:$SERVICE_ACCOUNT_EMAIL" --role="roles/artifactregistry.reader"

# 4. Create Artifact Registry repository
echo "Creating Artifact Registry repository..."
if ! gcloud artifacts repositories describe $REPOSITORY --location=$REGION > /dev/null 2>&1; then
    gcloud artifacts repositories create $REPOSITORY \
    --repository-format=docker \
    --location=$REGION \
    --description="Docker repository for Cloud Build Python application"
else
    echo "Artifact Registry repository '$REPOSITORY' already exists."
fi

echo "Infrastructure setup complete."
