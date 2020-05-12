# Interception Core Handler description
The "Interception Core Handler" is used to retrieve information about VoIP (calls information 
and interception), following of a LEA (Law Enforcement Agency) request. 

Interception software makes use of SeVoC (VoIP) and Polycube PacketCapture.

## Table of Contents
- [Architectural description](#architectural-description)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)

# Architectural description
This code implements "INTERCEPTION" agent (Interception Core Handler) on the Virtual Network 
Function (VNF) side.

```
       VNF          +        ContextBroker     +     SecurityController
                    |                          |
+--------------+    |  +-------------+         |     +-----------------+
| LocalManager |    |  |    Kafka    |         |     |      IADMF      |
+--------------+    |  +-------------+         |     +-----------------+
                    |                          |
|--------------|    |  |-------------|         |
| INTERCEPTION |    |  |   Logstash  |         |
|--------------|    |  |-------------|         |
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

"INTERCEPTION" agent is composed by three modules:
- a "REST SERVER" to receive request as "start interception"/"stop interception" with user-ID 
  of user to be intercepted
- an "IP ADDRESS/PORT FETCHER" : using user-ID and "VoIP Ubitech software" log, it fetches 
  ip address/port (src/dst) of user to be intercepted
- "POLYCUBE HANDLER" is used to set parameters to Polycube ("packetcapture") and start/stop 
  interception

# Installation
1. Prerequisite

- `Python3`
- `pip3`
- `Polycube` - https://polycube-network.readthedocs.io/en/latest/

2. Clone the repository

```bash
git clone https://gitlab.com/astrid-repositories/wp2/interception-data-agent.git
```

3. Install

```bash
cd interception-data-agent/interception_core_handler
bash ./scripts/install.sh
```

# Configuration
There are two methods to set up "Interception Core Handler": modifing directly the [configuration file](#configuration-by-file) or using the [configuration script](#configuration-by-script).

## Configuration by file
The software configuration can be done using the file "configurationFile.conf" in the "config" folder (interception-data-agent/interception_core_handler/config/configurationFile.conf).

The configuration file is in JSON format.
All parameters are in the "parameters" scope.
Following is the description of every field:

```
- loggerLevel : set up the level of debug between "INFO", "WARN", "DEBUG", "ERROR"
- interceptionInterfaceName : network interface used to intercepted VoIP traffic
- savedInterceptionPath : where "pcap" file (intercepted VoIP stream) is saved
- restServer : set up IP address and port on where "Interception Core Handler" recives requests to active/stop interception
- kafkaServer : Kafka IP address and port (usually outside the VM)
- logVoIPServer : deals with VoIP software log (correlation between "User VoIP number"/"User IP address")
  -- path : path where is the log file
  -- name : name of the log file
  -- readingTimeOut : sleeping time before log file reading (default 0.5 seconds)
- interceptionTools : specify what tool use to VoIP interception. Set flag between "true" (in use) and "false" (not in use)
```

## Configuration by script
Use the script ("configure.sh") in "./scripts" folder

```bash
cd interception-data-agent/interception_core_handler
bash ./scripts/configure.sh -h
```

```bash
-h                    Display this message
-d DEBUG_LEVEL        Debug level: INFO, WARN, DEBUG (default), ERROR
-i INTERFACE          Interface used to capture VoIP traffic,
                          empty value (default) is for "all interfaces"
-p PATH               Path where interceptions are saved
-a REST_IP            IP address of local REST listen server,
                          default is empty value
-b REST_PORT          Port of local REST listen server, default 5003
-e POLYCUBE_IP        Local Polycube IP address, default "127.0.0.1"
-f POLYCUBE_PORT      Local Polycube port, default 9000
-g KAFKA_IP           Kafka IP address, default is empty value, not used
-k KAFKA_PORT         Kafka port, default is 5002
-w KAFKA_TOPIC        Kafka topic used for communication with Kafka broker
-m LOG_PATH           Path of VoIP log file (folder)
-p LOG_FILENAME       Name of VoIP log file
-t LOG_READ_TIME      Timeout for execution of one VoIP log file reading cycle
-u ENABLE_POLYCUBE    Enable/disable Polycube PacketCapture for interception,
                          allowed values: true (active) / false (deactive - default)
-z ENABLE_LIBPCAP     Enable/disable Libpcap for interception,
                          allowed values: true (active - default) / false (deactive)

* If not specified, default value is used*


```

# Usage

```bash
cd interception-data-agent/interception_core_handler
bash ./scripts/run.sh
```

