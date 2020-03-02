# Interception Data Agent description
The "Interception Data Agent" is a software developed in the Astrid Project. 
The code is used to retrieve information about VoIP (calls information and interception), 
following of a LEA (Law Enforcement Agency) request. 
The interception software makes use of SeVoC (VoIP) and Polycube PacketCapture.

## TAble of Contents
- [Interception Data Agent]
- [Architecture description]
- [Installation]
- [Usage]

# Architecture description

This code implements "INTERCEPTION" agent on the Virtual Network Function (VNF) side.

       VNF          +        ContextBroker     +     SecurityController
                    |                          |
|--------------|    |  |-------------|         |     |-----------------|
| LocalManager |    |  |    Kafka    |         |     |      IADMF      |
|--------------|    |  |-------------|         |     |-----------------|
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

2. Clone the repository

```bash
git clone https://gitlab.com/astrid-repositories/wp2/interception-data-agent.git
cd context-broker-apis
```

# Usage

```bash
python3 interceptionMain.py
```

