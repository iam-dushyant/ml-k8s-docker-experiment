# Steps to restart GCP

## Introduction
This document is written to log restart steps after ```terraform destroy``` at the 
end of the day and/after each checkpoint, where the Infrastructure is destroyed to 
save unused costs.

In this project, the IaC constructed through Terraform is -
```
Artifact Registry - Docker image
Kubernetes - GKE Autopilot
HPA, Gatekeeper, Pods
```

After clean up, the high-level steps for restarting/reconstructing Infrastucture would be -
1. Authenticate to GCP
2. Initialise Terraform
3. terraform apply
4. Verify cloud infrastructure
5. Build Docker image
6. Push image → Artifact Registry
7. Connect kubectl → new GKE cluster
8. Recreate Kubernetes workload
9. Verify application
10. Recreate session-specific controls

## 1. Initialisation
The parameters for this project are -
```
Project:     k8s-docker-ml-dev
Region:      europe-west1
Repository:  ml-platform
Image:       ml-platform
Tag:         v{X}
```
where ```{X}``` is the version number

Therefore, on Terminal,
```
export PROJECT_ID="k8s-docker-ml-dev"
export REGION="europe-west1"

export REPO="ml-platform"
export IMAGE="ml-platform"
export TAG="v3"
```

## 2. Point to GCP project
```
gcloud config set project "$PROJECT_ID"
```
A Terraform state was created to be able to deploy this as and when required.
Deploy Terraform infrastructure by -
```
terraform init
```
Check Terraform state list by -
```
terraform state list
```
Validate, plan and apply the Terraform -
```
terraform validate
terraform plan -out=tfplan
terraform apply tfplan
```
## 3. Verify the actual GCP resources
GKE -
```
gcloud container clusters list \
  --project="$PROJECT_ID"
```
Artifact Registry -
```
gcloud artifacts repositories list \
  --project="$PROJECT_ID" \
  --location="$REGION"
```

## 4. Verify docker image in Artifact Registry
```
gcloud artifacts docker images list \
  "$REGION-docker.pkg.dev/$PROJECT_ID/$REPO" \
  --include-tags
```
If the image is not present, then rebuild the docker image.

```
export IMAGE_URI="$REGION-docker.pkg.dev/$PROJECT_ID/$REPO/$IMAGE:$TAG"
```
Authenticate Docker to Artifact Registry -
```
gcloud auth configure-docker "$REGION-docker.pkg.dev"
```
Build the docker image -
```
docker buildx build \
  --platform linux/amd64 \    # AMD64 for Apple Silicon
  -t "$IMAGE_URI" \
  --load \
  .
```
Push the docker image
```
docker push "$IMAGE_URI"
```

## 5. Kubernetes in GCP
Verify the Kubernetes cluster to check the entry point -
```
gcloud container clusters get-credentials "$CLUSTER" \
  --region="$REGION" \
  --project="$PROJECT_ID"
```
Then check -
```
kubectl config current-context
```
and
```
kubectl get nodes
kubectl get all -A
```
Before applying it, verify -
```
grep -n "image:" k8s/deployment.yaml
```
Deploy the application -
```
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```
Once deployed, verify -
```
kubectl get deployment -n ml-platform
kubectl get service -n ml-platform
```
Reapply the Horizontal Pod Autoscaling (HPA) - 
```
kubectl apply -f k8s/hpa.yaml
```