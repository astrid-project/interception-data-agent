# Artifact

Use the file ( [deployment_artifact.yaml](./deployment_artifact.yaml) ) to deploy:
* namespace
* configmap
* pods
* services 

## Namespace

The artifact creates a namespace with name "interception" and this is used for the deployments of every elements (configmap, pods and services)

## Configmap

The configmap is used to configure ElasticSearch and Kibana on "Lea Interface" pod

## Pods

The deployment of the artifact create three pods:
* Interception Request Handler
  This is the pod used to receive requests from LEA (start/stop interception about a specific user). This pod exposes a webserver to LEA requests and it is connected to Astrid Kafka to send communication to the Astrid Security Controller. The Interception Request Handler is based on only one container

* Interception Core Handler
  The pod has the task of physically starting/stopping the interception, fetching intercepted user information (missing call, starting call date, etc) and remote sanding data. The Interception Core Handler is connected to the Astrid Context Broker to be controlled and to the LEA Interface to send data.
This pod is composed by three containers.

* Lea Interface 
  The last pod deployed by the artifact is the Lea Interface. This is in place of LEA and it receives data from Interception Core Handler and save user information in ElasticSearch DB and the call interception in a specific directory. 
A Kibana installation is used to show user information data.
This pod is composed by four containers.

## Services

Every POD has a service connected to it.

## Create the Artifact

Use [create_global_artifact.sh](./create_global_artifact.sh) to remove old global artifact and create a new one (if you do some changes to one or more file in [artifacts](./artifacts) directory)

