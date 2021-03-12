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

## PODs configuration and start

Use the artifact files to configure and to start different PODs.
The main important parameters are inside the "env" scope. Change these values following the instructions below.

### "Request Handler POD" configuration

Log level can be changed modifying the value between "DEBUG" or "INFO"

    - name: LOGGERLEVEL
      value: "DEBUG"

"Request Handler" receives request from "LEA" actor by REST API.
The server used is specified by IP address ( "0.0.0.0" is for "listen to every interfaces ) and port

    - name: RESTSERVERADDRESS
      value: "0.0.0.0"
    - name: RESTSERVERPORT
      value: "5004"

The message received from LEA must be sent to "Security Controller" using Kafka.
For debug purpouse it is possible to by-pass this function and send the message directly to "Context Broker".
Enable only one of the two methods.
To disable specify "0.0.0.0" for IP address and "0" for port.

    - name: KAFKAADDRESS
      value: "kafka-service.astrid-kube"
    - name: KAFKAPORT
      value: "9092"
    - name: KAFKATOPIC
      value: "interception"
    - name: CONTEXTBROKERADDRESS
      value: "0.0.0.0"
    - name: CONTEXTBROKERPORT
      value: "0"
    - name: CONTEXTBROKERUSER
      value: "astrid"
    - name: CONTEXTBROKERPASSWORD
      value: "none"


### "Core Handler POD" configuration

Define logger level between "INFO" and "DEBUG" options

    - name: LOGGERLEVEL
      value: "DEBUG"

Set the name of the interface used for interception

    - name: INTERFACE
      value: "eth0"

Set directory where interception is temporary saved (cache) during the trasmission to "LEA interface"

    - name: INTERCEPTIONPATH
      value: "/root/interceptions/"

Set the IP address and port used by the "Core Handler" REST server to receive requests from "LCP".
It is also possible to handly send REST requests using for example "curl".
The "0.0.0.0" values is for "every interfaces" on server.

    - name: RESTSERVERADDRESS
      value: "0.0.0.0"
    - name: RESTSERVERPORT
      value: "5003"

Set the Polycube IP address and port

    - name: POLYCUBEADDRESS
      value: "127.0.0.1"
    - name: POLYCUBEPORT
      value: "9000"

"Core Handler" remotely saves two type of information: interception actions (ex. start of call, missing call, etc.) and interception call ("pcap" file).
Interception actions info are always sent to "LEA Interface" by Logstash use.
Instead Interception call file can be moved to "LEA Interface" using diffent methodology: Logstash, Kafka or remote TCP server.
Enable only one of these three methods, disabling the two not used.
To disable method set IP address to "0.0.0.0" and port to "0".
WARNING: LOGSTASH IP address is used also for interception action info so it is always defined.
LOGSTASHMSGPORT is used for interception action info.
LOGSTASHDATAPORT is used for interceptino call file. 

    - name: KAFKAADDRESS
      value: "0.0.0.0"
    - name: KAFKAPORT
      value: "5002"
    - name: KAFKATOPIC
      value: "interception"
    - name: LOGSTASHADDRESS
      value: "lea-interface"
    - name: LOGSTASHMSGPORT
      value: "5959"
    - name: LOGSTASHDATAPORT
      value: "5960"
    - name: LOGSTASHVERSION
      value: "1"
    - name: TCPSERVERADDRESS
      value: "0.0.0.0"
    - name: TCPSERVERPORT
      value: "0"


Set directory where VoIP log file is

    - name: LOGVOIPPATH
      value: "./logs/"

Set name of the VoIP log file

    - name: LOGVOIPFILENAME
      value: "containerLogs.log"

Set timeout for polling reading of VoIP log file (read only the new part of the file)

    - name: LOGVOIPREADINGTIME
      value: "0.5"

The capture of the interception traffic can be done by "Polycube Packet Capture" or "Libpcap".
Enable only one of these two methods.

    - name: POLYCUBEISENABLED
      value: "true"
    - name: LIBPCAPISENABLED
      value: "false"


### "LEA Interface POD" configuration

Set logger level between "Info" or "Debug"

    - name: LOGGERLEVEL
      value: "DEBUG"

Set server IP address and port to receive the interception call file.
Use "0.0.0.0" to enable TCP connection listening from all interfaces.
Disable TCP server using "0" as port parameter.

    - name: TCPSERVERADDRESS
      value: "0.0.0.0"
    - name: TCPSERVERPORT
      value: "5004"

Set Kafka IP address, port and topid to use for receiving interception call file (pcap).
Disable Kafka client by "0" value as port parameter.

    - name: KAFKAADDRESS
      value: "kafka-service.astrid-kube"
    - name: KAFKAPORT
      value: "0"
    - name: KAFKATOPIC
      value: "interception"


