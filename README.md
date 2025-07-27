# Project Planner (Midterm-for-technion)

## Introduction

As a midterm project, may I have the distinct honor to present to you **Project Planner**.

With **Project Planner** You can calculate the amount of compute resources needed for your project.

There are currently 3 main functionalities:
### Inventory Items ###
An _item_ is made out of:
* Name
* CPU count
* RAM amount
* Hard Disk size
* Price

### Projects ###
A _project_ is made out of:
* Name
* Types and quantities of _invnetory items_

### Statistics ###
In the end you get calculations which might help you plan your projects more effectively.

## Requirements
Although the project in built on Python 3.13 (and Flask 3.1.1), it has automation to compile it into a Docker image.
It shouldn't worry you.

The automations were built for Bash and were tested on an Ubuntu 22.04 machine, but it should normally run in any modern Linux machine with preinstalled docker.

The endgame deployment should run the project in AWS in HA mode, so please make sure to have an account before deployment.

## Deployment

After cloning the repo locally, please `cd <repo>/Linux`.
Then please run the 3 bash scripts in order:
```
./01-build_and_run_docker.sh
./02-install_aws_cli.sh
./03-uploads_to_AWS
```

More details in the Linux section.

Go get them, Tigers!