export PROJECT_ID=$(gcloud config get-value project)
export LOCATION=us-east4

gunicorn --bind :8080 --workers 1 --threads 8 --timeout 15 app.main:app