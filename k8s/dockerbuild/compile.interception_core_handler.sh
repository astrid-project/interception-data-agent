#!/bin/bash

IMAGE_NAME=infocomsrl/interception-core-handler
VERSION=0.1
DOCKERFILE=dockerbuild/Dockerfile.interception_core_handler

cd ..

echo "remove old local build..."
docker image rm $IMAGE_NAME:$VERSION 

echo "compile new local build..."
docker build --tag $IMAGE_NAME:$VERSION -f $DOCKERFILE .

#echo "push new local build on remote registry..."
#docker push $IMAGE_NAME:$VERSION 
