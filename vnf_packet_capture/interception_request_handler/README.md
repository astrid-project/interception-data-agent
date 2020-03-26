# Interception Request Handler description
The "Interception Request Handler" is a software developed in the Astrid Project. 
The code is used to receive request of interception by LEA (Law Enforcement Agency) and send an active/deactive command to the "Interception Core Handler", using Context-Broker API

## Table of Contents
- [Architecture description]
- [Installation]
- [Configuration]
- [Usage]

# Architecture description

This code implements "INTERCEPTION HANDLER" agent on Security Controller.

```
       VNF          +        ContextBroker     +     SecurityController
                    |                          |
+--------------+    |  +-------------+         |     +-----------------+
| LocalManager |    |  |    Kafka    |         |     |  INTERCEPTION   |
+--------------+    |  +-------------+         |     |     HANDLER     |
                    |                          |     +-----------------+
|--------------|    |  |-------------|         |
| Interception |    |  |   Logstash  |         |
| Core Handler |    |  |-------------|         |
|--------------|    |                          |
                    |                          |
|--------------|    |  |----------------|      |
|   Logstash   |    |  | ContextManager |      |
|--------------|    |  |----------------|      |
                    |                          |
|--------------|    |                          |
|   Polycube   |    |                          |
|--------------|    |                          |
                    |                          | 
```

"Interception Request Handler" acts as a proxy server: receive requests from LEA and move
them to the "Interception Core Handler" using the "Context Broker API"

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
cd interception-data-agent/interception_request_handler
bash ./scripts/install.sh
```

# Configuration
There are two methods to set up "Interception Request Handler": modifing directly the configuration file or using the configuration script.

## Configuration by file
The software configuration can be done using the file "configurationFile.conf" in the "config" folder (interception-data-agent/interception_request_handler/config/configurationFile.conf).
The configuration file is in JSON format.
All parameters are in the "parameters" scope.
Following is the description of every field:

```
- loggerLevel : set up the level of debug between "INFO", "WARN", "DEBUG", "ERROR"
- restServer : IP address and port on which program receives interception requests from LEA
- contextBroker : IP address and port of the "Context Broker API"
```

## Configuration by script
Use the script ("configure.sh") in "./scripts" folder

```bash
cd interception-data-agent/interception_request_handler
bash ./scripts/configure.sh -h
```

```bash
-h                    Display this message
-d DEBUG_LEVEL        Debug level: INFO, WARN, DEBUG (default), ERROR
-a REST_IP            IP address of local REST listen server,
                          default "0.0.0.0", all addresses
-b REST_PORT          Port of local REST listen server, default 5003
-e CONTEXTBROKER_IP   Local ContextBroker IP address, default value is empty
-f CONTEXTBROKER_PORT Local ContextBroker port, default value is empty
-u USER               User to use to connect to ContextBroker, default value is "astrid"
-p PASSWORD           Password to use to connect to ContextBroker

* If not specified, default value is used*

```

# Usage

```bash
cd interception-data-agent/interception_request_handler
bash ./scripts/run.sh
```

