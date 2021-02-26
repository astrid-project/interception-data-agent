# Artifacts

"Lawful Interception" code architecture is composed by three PODs: "Request Handler POD", "Core Handler POD" and "LEA Interface POD".
"Request Handler POD" is composed only by one container, that is the "Request Handler" module.
"Core Handler POD" is instead the union of three different containers: 
	- "Core Handler"
	- "Local Control Plane"
	- "Polycube"
"LEA Interface POD" has two containers and a configmap file ("lea_interface_configmap.yaml"): 
	- "LEA Interface POD"
	- "Logstash"


