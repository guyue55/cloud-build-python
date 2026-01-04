# list repositories
gcloud artifacts repositories list --location=us-central1

# create repository
gcloud artifacts repositories create cloud-service \
  --repository-format=docker \
  --location=us-central1 \
  --description="Docker repository"