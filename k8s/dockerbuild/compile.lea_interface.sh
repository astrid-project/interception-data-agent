#!/bin/bash

IMAGE_NAME=infocomsrl/lea-interface
VERSION=0.1
DOCKERFILE=dockerbuild/Dockerfile.lea_interface

cd ..

echo "remove old local build..."
docker image rm $IMAGE_NAME:$VERSION 

echo "compile new local build..."
docker build --tag $IMAGE_NAME:$VERSION -f $DOCKERFILE .

#echo "push new local build on remote registry..."
#docker push $IMAGE_NAME:$VERSION 
