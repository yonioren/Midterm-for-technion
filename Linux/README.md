# Linux

Ah, I see you are persons of details.

Very well then...

## 01-build_and_run_docker.sh

This script will compile the python code into a docker image and run it locally as a demo.

It will find the source code, the Dockerfile and the requirements file under the Python directory and wuuushhhhh!
A docker image and a container named `demo` should be available.

Please run with `--force` if you want to build it multiple times.

In the end it will even be friendly enough to provide you with the URL.

## 02-install_aws_cli.sh

In here we set the environment to allow deployment to AWS.

```This is a good time to press that AWS academy sandbox button```.

You will be required to copy-paste the AWS-CLI section details into the open file and save.
If you don't know VIM, start by learning it. NANO IS AWEFUL!

You would be requested to select an AWS region. Embrace yourselves!

## 03-uploads_to_AWS.sh

>> It's business.
>> 
>> It's business time.
>
> _Business Time - Flight of the Conchords_

This script will:
1. Upload the docker image to the cloud.
2. Find the latest Amazon Linux 2 64bit on GP2 image in the selected region.
3. Deploy the AWS environment.
4. Run Project Planner.
5. Give you a URL to surf to.

> Please note there is a bit of JMESPath - it's like JSONPath but less friendly
