#!/bin/bash

. CONSTS

aws cloudformation validate-template --template-body file://network-ha.yaml

#aws cloudformation create-stack \
#  --stack-name my-network-stack \
#  --template-body file://network-ha.yaml
#
#aws cloudformation wait stack-create-complete \
#  --stack-name my-network-stack
#
#aws cloudformation describe-stacks \
#  --stack-name my-network-stack \
#  --query "Stacks[0].Outputs"
