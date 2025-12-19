#!/bin/bash

PROJECT_ID=$(gcloud config get-value project) # 自动获取当前项目 ID

# list repositories
gcloud artifacts repositories list --location=us-central1

# list images
gcloud artifacts docker images list us-central1-docker.pkg.dev/${PROJECT_ID}/test
gcloud artifacts docker images list us-central1-docker.pkg.dev/${PROJECT_ID}/my-repository