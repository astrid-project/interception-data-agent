#!/bin/bash

echo "removing \"deployment_artifact.yaml\" file..."

rm deployment_artifact.yaml

echo "... done"



echo "creating new deployment_artifact.yaml file..."

cat artifacts/namespace.yaml >> ./deployment_artifact.yaml
echo "---" >> ./deployment_artifact.yaml
cat artifacts/lea_interface_configmap.yaml >> ./deployment_artifact.yaml
echo "---" >> ./deployment_artifact.yaml
cat artifacts/request_handler_pod.yaml >> ./deployment_artifact.yaml
echo "---" >> ./deployment_artifact.yaml
cat artifacts/core_handler_pod.yaml >> ./deployment_artifact.yaml
echo "---" >> ./deployment_artifact.yaml
cat artifacts/lea_interface_pod.yaml >> ./deployment_artifact.yaml
echo "---" >> ./deployment_artifact.yaml
cat artifacts/request_handler_service.yaml >> ./deployment_artifact.yaml
echo "---" >> ./deployment_artifact.yaml
cat artifacts/core_handler_service.yaml >> ./deployment_artifact.yaml
echo "---" >> ./deployment_artifact.yaml
cat artifacts/lea_interface_service.yaml >> ./deployment_artifact.yaml
echo "---" >> ./deployment_artifact.yaml

echo "... done"


