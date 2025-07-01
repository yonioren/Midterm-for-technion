#!/bin/bash

. CONSTS

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

##### DOCKERRUN.AWS.JSON for Beanstalk

sed "s#@@@ DockerImageName - WILL BE OVERRIDDEN BY SCRIPT @@@#${ECR_URI}:${TAG}#" \
  "${AWS_BEANSTALK_JSON_TEMPLATE}" > "${AWS_BEANSTALK_JSON_SRC}"

##### S3 #####

### Upload S3
if ! aws s3 ls s3://${AWS_BUCKET_NAME}
then
  aws s3 mb s3://${AWS_BUCKET_NAME}
fi

if ! aws s3 ls s3://${AWS_BUCKET_NAME}
then
  echo "Something went wrong while creating the s3 bucket"
  exit 2
fi

aws s3 cp "${AWS_BEANSTALK_JSON_SRC}" "s3://${AWS_BUCKET_NAME}/${AWS_BEANSTALK_JSON_DST}"

if [ $? -ne 0 ]
then
  echo "Something went wrong while uploading the version data into S3"
  exit 3
fi


##### Cloudformation #####

#aws cloudformation validate-template --template-file "file://${AWS_CF_TEMPLATE}" 
aws cloudformation deploy --template-file "${AWS_CF_TEMPLATE}" --stack-name stackname --capabilities CAPABILITY_NAMED_IAM --parameter-overrides "S3BucketName=${AWS_BUCKET_NAME}" "S3PathInBucket=${AWS_BEANSTALK_JSON_DST}"
echo aws cloudformation deploy --template-file "${AWS_CF_TEMPLATE}" --stack-name stackname --parameter-overrides "S3BucketName=${AWS_BUCKET_NAME}" "S3PathInBucket=${AWS_BEANSTALK_JSON_DST}"

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
