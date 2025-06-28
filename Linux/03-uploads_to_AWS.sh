#!/bin/bash

. CONSTS

AWS_DIR="$(dirname $(readlink -f $0))/../AWS"
AWS_TEMPLATE="${AWS_DIR}/infrastructure_template.yaml"
AWS_DEST="${AWS_DIR}/Cloudformation.yaml"

# Create ECR private repo if necessary
if ! aws ecr describe-repositories --repository-names "$REPO_NAME" --output text >/dev/null 2>&1
then
  echo "Repository '$REPO_NAME' does not exist. Creating it..."
  aws ecr create-repository --repository-name "$REPO_NAME"
  echo "Repository '$REPO_NAME' created."
fi

# Pull the URI of the repository in order to allow off-aws work against it
ECR_URI="$(aws ecr describe-repositories --repository-names "${REPO_NAME}" --query "repositories[0].repositoryUri" --output text)"

# docker login
ECR_URI_HOST=$(echo "${ECR_URI}" | cut -d'/' -f1)
aws ecr get-login-password | docker login --username AWS --password-stdin "${ECR_URI_HOST}"

# upload image
docker tag "${SOURCE_IMAGE}:${TAG}" "${ECR_URI}:${TAG}"
docker push "${ECR_URI}:${TAG}"

# Sometimes it takes some time for the image to be available
sleep 5

if aws ecr describe-images --repository-name "${REPO_NAME}" --image-ids "imageTag=${TAG}"
then
  echo "The version was successfully uploaded to ECR"
else
  echo "Something went wrong while uploading the image to ECR. Aborting"
  exit 1
fi

sed "s#@@@ DockerImageName - WILL BE OVERRIDDEN BY SCRIPT @@@#${ECR_URI}:${TAG}#" ${AWS_CF_TEMPLATE} > ${AWS_CF_DEST}

if [ ! -f ${AWS_CF_DEST} ]
then
  echo "Something went wrong while creating the Cloudformation yaml. Aborting"
  exit 2
else
  echo "The app is ready to be deployed to AWS!"
fi