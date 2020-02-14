"""
README.txt

developed by @Infocom - 2020
info: guerino.lamanna@infocomgenova.it
"""

This code implements "INTERCEPTION" on the Virtual Network Function (VNF) side.

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

"INTERCEPTION" is composed by three modules:
- a "REST SERVER" to receive request as "start interception"/"stop interception" with user-ID 
  of user to be intercepted
- an "IP ADDRESS/PORT FETCHER" : using user-ID and "VoIP Ubitech software" log, it fetches 
  ip address/port (src/dst) of user to be intercepted
- "POLYCUBE HANDLER" is used to set parameters to Polycube ("packetcapture") and start/stop 
  interception


