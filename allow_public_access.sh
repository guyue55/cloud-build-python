# Replace these variables with your actual project details.
PROJECT_ID=$(gcloud config get-value project)
REPOSITORY="cloud-service"
export PROJECT_ID=${PROJECT_ID}
export REGION="us-central1"
export SERVICE_NAME="cloud-build-python"

#echo "Allow public access"
gcloud run services add-iam-policy-binding --region=${REGION} --project=${PROJECT_ID} --member=allUsers --role=roles/run.invoker ${SERVICE_NAME}
