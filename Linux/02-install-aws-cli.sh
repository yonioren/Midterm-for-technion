#!/bin/bash

# Install awscli if not already installed
if ! command -v aws &> /dev/null; then
  echo "Downloading and installing AWS CLI"
  curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "/tmp/awscliv2.zip"
  cd /tmp/
  unzip awscliv2.zip
  sudo ./aws/install
fi

# Create ~/.aws directory with correct permissions
mkdir -p ~/.aws
chmod 700 ~/.aws

# Create ~/.aws/credentials with placeholder and correct permissions
echo "# Please paste the connection information from the LAB (AWS Details)" > ~/.aws/credentials
chmod 600 ~/.aws/credentials

# Open credentials file in vim
vim ~/.aws/credentials

# Confirm
if aws sts get-caller-identity
then
  echo "The AWS cli environment is ready"
fi
