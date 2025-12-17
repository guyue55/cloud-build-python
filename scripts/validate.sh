
#!/bin/bash

# 指定 Service Account 进行部署
SERVICE_NAME=cloud-build-python
REGION=us-central1

gcloud run services describe ${SERVICE_NAME} --region ${REGION} --format='value(spec.template.spec.serviceAccountName)'