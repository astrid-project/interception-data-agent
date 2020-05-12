# Interception Data Agent introduction
The "Interception Data Agent" is a software developed inside the Astrid Project.
Its use is regarding to retrieve information about VoIP (call information and interception) following of a LEA (Law Enforcement Agency) request.

The interception software makes use of SeVoC (VoIP) and Polycube PacketCapture.
Usually configuration is composed by "Interception Data Agent", "Security Controller", "Context Broker", "Polycube Packet Capture", "Elastic" software suite ("Logstash", "ElasticSearch") and "Kafka".

If not diffent explained, all configuration steps, described below, referes to previous case.
In this manual you can find description of the software, its installation, configuration and usage. 

Morover also steps to configure "Elastic software suite" in a basic testbed is presented.

## Table of Contents
- [Software description](#software-description)
- [Architectural description](#architectural-description)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Elastic/Kafka configuration](#elastic/kafka-configuration)

# Software description
"Interception Data Agent" is composed by three main python softwares: 
- Interception Core Handler - see ["interception_core_handler"](./interception_core_handler/README.md) content for more information about install, use and architecture
- Interception Request Handler - see ["interception_request_handler"](./interception_request_handler/README.md) content for more information about install, use and architecture
- LEA interface - see ["lea_interface"](./lea_interface/README.md) content for more information about install, use and architecture

# Architectural description

```
                                                                           LEA requests
       VNF          +   Context Broker     +    SecurityController   +        |
    (Exec-env)      |                      |                         |        | 
                    |                      |                         |        V
+--------------+    |  +-------------+     |     +-------------+     |    +-----------------+
| Interception |    |  |   Context   |     |     |  Security   |     |    |  Interception   |
|     Core     | <---- |   Broker    | <-------  |  Controller | <------- |     Request     |
|    Handler   |    |  +-------------|     |     +-------------+     |    |     Handler     |   
+--------------+    |                      |                         |    +-----------------+
     ^   ^   |      |                      |                         |
     |   |   |      + -------------------- + ----------------------- + ------------------------ 
     |   |   |                            
     |   |   +-------+                     +                         +
     |   +----+      |    +------------+   |      +-----------+      |     +--------------+
+----------+  |      |    |            |   |      |           |      |     |              |      
| Packet   |  |      +--> |  Logstash  | -------> |   Kafka   | ---------> |   Logstash   |     
| Capture  |  |      |    |            |   |      |           |      |     |              |
|   or     |  |      |    +------------+   |      +-----------+      |     +--------------+
| Libpcap  |  |      |                     |                         |
+----------+  |      |                     |                         |
+--------+    |      |                     |                         |     +--------------+
|  VoIP  | ---+      +---------------------------------------------------> |     LEA      |
|  logs  |                                 |                         |     |   Interface  |
+--------+                                 |                         |     +--------------+
                                           |                         |
                                           +                         +

```

General architecture is composed of three main modules (["Interception Request Handler"](./interception_request_handler/README.md), ["Interception Core Handler"](./interception_core_handler/README.md) and ["LEA Interface"](./lea_interface/README.md)). To correctly works, they need to be installed in an Astrid deploymnent. In the figure upon there is the rappresentation of a common complete installation.

As we can see, "Interception Data Agent" software is integrated with other Astrid components and it is addressed to the following data flow:
- LEA sends request of intercetion (start or stop) to the "Interception Request Handler". The message contains information about intercepted user identification, Service Provider of the service used by user and Service.
- "Interception Request Handler" is the interface between the LEA and the Astrid framework. It receives LEA request and sends it to the "Security Controller" by Kafka broker.
- The "Security Controller" is capable to receive message from "Interception Request Handler" and using the "Context Broker", move the request to the "Interception Core Handler".
- The "Interception Core Handler" is the main important module in "Interception Data Agent". It receives request by "Context Broker" and it collects interception user data by reading VoIP log information (start call, missing call, etc). Moreover it is also able to intercept VoIP traffic and to send capture result (pcap file) to the LEA using "Elastic" chain or TCP channel.
- Last "Interception Data Agent" module is named "LEA Interface" and it is used for debugger purpose.

It is a server to save VoIP interception as it is the LEA, just to check captured data. In fact LEA mechanism to save interception data (calling data and interception) is out of scope of Astrid project. 


# Installation
- see ["interception_core_handler"](./interception_core_handler/README.md) directory for "Interception Core Handler"
- see ["interception_request_handler"](./interception_request_handler/README.md) directory for "Interception Request Handler"

# Configuration
- see ["interception_core_handler"](./interception_core_handler/README.md) directory for "Interception Core Handler"
- see ["interception_request_handler"](./interception_request_handler/README.md) directory for "Interception Request Handler"


# Usage
- see ["interception_core_handler"](./interception_core_handler/README.md) directory for "Interception Core Handler"
- see ["interception_request_handler"](./interception_request_handler/README.md) directory for "Interception Request Handler"

# Elastic/Kafka configuration
- see ["elastic_kafka_configuration"](./elastic_kafka_configuration/README.md) directory for config file and explanation.