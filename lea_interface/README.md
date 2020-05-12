# LEA interface description
LEA has to interact with Astrid framework to get user call interception data. The "LEA interface" is a module of "Interception Data Agent" that emulate behaviour of LEA.

In more specific way, it is composed by an "ElasticSearch" database, to collect all interception information (missing calls, start calls, end calls, etc.) and a Python server to receive interception streams and save it on file.

## Table of Contents
- [Architecture description](#architectural-description)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)


# Architecture description
This code implements "LEA Interface" as a Python module. It provides a TCP server and a Kafka client to receive VoIP interception stream data from "Interception Core Handler".

Calls interception information (start calls, stop calls, missing calls, etc) are saved into "ElasticSearch" using a directly connection from Logstash.

"LEA Interface" can be used as a TCP server or a Kafka client to receive  interceptions.
TCP server is the best solution, because is more efficient: data are directly sent from "Interception Core Handler" to "LEA interface" without any type of manipulation. For every interception only one addictional message will be sent at the starting of the TCP stream (carrying the interception). This message has addictional information about the intercepted user, the provider and the same interception.

On the other hand, "LEA Interface" can be used as a "Kafka" client. In this case the interception will be carried as a bulk of Kafka messages. Every part of the interception must be encoded before be sent and decoded on the receiving phase.

```                 
                                              
+--------------+           +-------------+           +-----------------+
| Interception | ---//---> |  Logstash   | ---//---> |  ElasticSearch  |
|    Core      |           +-------------+           +-----------------+
|   Handler    |                                     +-------------+
+--------------+ ---//------------//----------//---> |     LEA     |
                           TCP or Kafka              |  Interface  |
                                                     +-------------+

```


# Installation
1. Prerequisite

- Python3
- pip3

2. Clone the repository

```bash
git clone https://gitlab.com/astrid-repositories/wp2/interception-data-agent.git
```

3. Install

```bash
cd interception-data-agent/lea_interface
bash ./scripts/install.sh
```

# Configuration
There are two methods to set up "LEA Interface": modifing directly the [configuration file](#configuration-by-file) or using the [configuration script](#configuration-by-script).

## Configuration by file
The software configuration can be done using the file "configurationFile.conf" in the "config" folder (interception-data-agent/lea_interface/config/configurationFile.conf).

The configuration file is in JSON format.

All parameters are in the "parameters" scope.
Following is the description of every field:

```
- loggerLevel : set up the level of debug between "INFO", "WARN", "DEBUG", "ERROR"
- tcpServer : IP address and port on which program receives interceptions
- kafkaServer : IP address and port on wich program receives interceptions, and topic for data receiver
```

To disable TCP or Kafka mode, set corresponding parameter to "" (empty string) for IP address and 0 (zero as a number) for port.

## Configuration by script
Use the script ("configure.sh") in "./scripts" folder

```bash
cd interception-data-agent/interception_request_handler
bash ./scripts/configure.sh -h
```

```bash
-h                    Display this message
-d DEBUG_LEVEL        Debug level: INFO, WARN, DEBUG (default), ERROR
-t TCP_IP             IP address of local TCP listen server,
                          default "0.0.0.0", all addresses
-u TCP_PORT           Port of local TCP listen server, default 5004
-g KAFKA_IP           Kafka IP address, default is empty value, not used
-k KAFKA_PORT         Kafka port, default is 5002
-w KAFKA_TOPIC        Kafka topic used for communication with Kafka broker


* If not specified, default value is used*


```

# Usage

```bash
cd interception-data-agent/lea_interface
bash ./scripts/run.sh
```

