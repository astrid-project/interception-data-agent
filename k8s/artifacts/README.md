# Artifacts

The files in this directory are all the artifacts used in the yaml file into upon directory and the script to create it.
Use the order of files to deploy all artifacts.

## List of files

Artifact to create the namespace ("interception"):
* [namespace.yaml](./namespace.yaml)

Artifact to load the configmap:
* [lea_interface_configmap.yaml](./lea_interface_configmap.yaml)

Artifacts to deploy every pod:
* [core_handler_pod.yaml](./core_handler_pod.yaml)
* [lea_interface_pod.yaml](./lea_interface_pod.yaml)
* [request_handler_pod.yaml](./request_handler_pod.yaml)

Artifacts to create the services:
* [core_handler_service.yaml](./core_handler_service.yaml)
* [lea_interface_service.yaml](./lea_interface_service.yaml)
* [request_handler_service.yaml](./request_handler_service.yaml)

