#!/bin/bash

###### https://www.awsacademy.com/vforcesite/LMS_Login

# Install awscli if not already installed
if ! command -v aws &> /dev/null; then
  echo "Downloading and installing AWS CLI"
  curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "/tmp/awscliv2.zip"
  cd /tmp/
  unzip awscliv2.zip
  sudo ./aws/install
  cd -
fi

# Create ~/.aws directory with correct permissions
mkdir -p ~/.aws
chmod 700 ~/.aws

# Create ~/.aws/credentials with placeholder and correct permissions
if [ ! -f ~/.aws/credentials ]
then
  echo "# Please paste the connection information from the LAB (AWS Details)" > ~/.aws/credentials
fi
chmod 600 ~/.aws/credentials

# Open credentials file in vim
sudo apt install vim
vim ~/.aws/credentials

# Confirm
if aws sts get-caller-identity
then
  echo "The AWS cli environment is ready"
fi

AWS_REGIONS="$(aws ec2 describe-regions --query "Regions[*].RegionName" --output text --region us-east-1)"

echo "Select the AWS region to deploy on"
select user_selection in ${AWS_REGIONS[@]}
do
  if [[ -n "${user_selection}" ]]
  then
    aws configure set region "${user_selection}"
    break
  else
    echo "Invalid selection"
    exit 1
  fi
done
