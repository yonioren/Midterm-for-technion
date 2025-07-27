#!/bin/bash

. CONSTS
DEMO_CONTAINER_NAME="demo"



case "$1" in
  "-f"|"--force")
    FORCE="true"
    echo "Using FORCE"
    ;;
esac

if [ ! -f "${PYTHON_DIR}/Dockerfile" ]
then
  echo "Could not find the Docker file"
  exit 127
fi

if [ ! -d "${PYTHON_DIR}/source" ]
then
  echo "Could not file the Python source code"
  exit 127
fi

if [ ! -f "${PYTHON_DIR}/requirements.txt" ]
then
  echo "Could not find the Python dependencies file"
  exit 127
fi

if [ "${FORCE}" == "true" ]
then
  docker kill "${DEMO_CONTAINER_NAME}" &>/dev/null
  docker rm "${DEMO_CONTAINER_NAME}" &>/dev/null
  docker rmi "${FULL_IMAGE_NAME}" &>/dev/null
fi

if [ -n "$(docker images -q "${FULL_IMAGE_NAME}" 2>/dev/null)" ]
then
  echo "The docker image already exists. run with --force to recreate"
else
  cd "${PYTHON_DIR}"
  docker build -t "${FULL_IMAGE_NAME}" .
  cd -
fi

if [ -z "$(docker images -q "${FULL_IMAGE_NAME}" 2>/dev/null)" ]
then
  echo "The ${FULL_IMAGE_NAME} image does not exist locally. aborting demo"
  exit 1
elif [ "$(docker inspect -f "{{.State.Running}}" "${DEMO_CONTAINER_NAME}" 2>/dev/null)" == "true" ]
then
  echo "The app is already running. run with --force to recreate"
else
  docker run -it -d --rm --name "${DEMO_CONTAINER_NAME}" -p 8666:8666 "${FULL_IMAGE_NAME}"
fi

if [ "${?}" -ne 0 ]
then
  echo "An error occurred while running the app"
else
  echo "The app is up. Please surf to http://127.0.0.1:8666 to access the site"
fi
