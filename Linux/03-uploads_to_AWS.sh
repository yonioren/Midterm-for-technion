#!/bin/bash

. CONSTS
AWS_CF_TEMPLATE="${AWS_DIR}/Cloudformation/template.yaml"
REPO_NAME="${IMAGE}" ### serves as IMAGE NAME in AWS #####

##### ECR #####

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
docker tag "${FULL_IMAGE_NAME}" "${ECR_URI}:${TAG}"
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

################## Get latest AmazonLinux AMI ID from region
# https://aws.amazon.com/blogs/compute/query-for-the-latest-amazon-linux-ami-ids-using-aws-systems-manager-parameter-store/
# LabRole
AMI_ID="$(aws ec2 describe-images --owners amazon --filters "Name=name,Values=amzn2-ami-hvm-*-x86_64-gp2" "Name=state,Values=available" --query "Images | sort_by(@, &CreationDate) | [-1].ImageId" --out=text)"

##### Cloudformation #####

aws cloudformation deploy --template-file "${AWS_CF_TEMPLATE}" --stack-name stackname --capabilities CAPABILITY_NAMED_IAM --parameter-overrides "EcrImageUrl=${ECR_URI}:${TAG}" "AmiID=${AMI_ID}"

# cloudformation reacte-stack \
#  --stack-name my-network-stack \
#  --template-body file://network-ha.yaml
#
#aws cloudformation wait stack-create-complete \
#  --stack-name my-network-stack
#
#aws cloudformation describe-stacks \
#  --stack-name my-network-stack \
#  --query "Stacks[0].Outputs"
