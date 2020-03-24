# Interception Core Handler description
The "Interception Core Handler" is used to retrieve information about VoIP (calls information 
and interception), following of a LEA (Law Enforcement Agency) request. 
Interception software makes use of SeVoC (VoIP) and Polycube PacketCapture.

# Table of Contents
- [Architectural description]
- [Installation]
- [Configuration]
- [Usage]

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
- Python3
- pip3

2. Clone the repository

```bash
git clone https://gitlab.com/astrid-repositories/wp2/interception-data-agent.git
```

3. Install

```
cd interception-data-agent/interception_core_handler
./scripts/install.sh
```

# Configuration
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

# Usage

```bash
cd interception-data-agent/interception_core_handler
./scripts/run.sh
```

