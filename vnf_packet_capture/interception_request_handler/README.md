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
cd interception-data-agent\interception_request_handler
./scripts/install.sh
```

# Configuration
The software configuration can be done using the file "configurationFile.conf" in the "config" folder (interception-data-agent/interception_request_handler/config/configurationFile.conf).
The configuration file is in JSON format.
All parameters are in the "parameters" scope.
Following is the description of every field:

```
- loggerLevel : set up the level of debug between "INFO", "WARN", "DEBUG", "ERROR"
- restServer : IP address and port on which program receives interception requests from LEA
- contextBroker : IP address and port of the "Context Broker API"
```

# Usage

```bash
cd interception-data-agent\interception_request_handler
./scripts/run.sh
```

