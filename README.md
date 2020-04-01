# Interception Data Agent description
The "Interception Data Agent" is a software developed in the Astrid Project. 
The code is used to retrieve information about VoIP (call information and interception) 
following of a LEA (Law Enforcement Agency) request. 
The interception software makes use of SeVoC (VoIP) and Polycube PacketCapture.

## Table of Contents
- [Software description](#software-description)
- [Architectural description](#architctural-description)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)

# Software description
"Interception Data Agent" is composed by two python software: 
- Interception Core Handler - see ["interception_core_handler"](./interception_core_handler/README.md) content for more information about install, use and architecture
- Interception Request Handler - see ["interception_request_handler"](./interception_request_handler/README.md) content for more information about install, use and architecture

# Architectural description

```
       VNF          +  SecurityController  +           ___LEA requests
    (Exec-env)      |                      |          / 
                    |                      |         \/
+--------------+    |  +-------------+     |     +-----------------+
| Interception |    |  |  Security   |     |     |  Interception   |
|     Core     | <---- |  Controller | <-------- |     Request     |
|    Handler   |    |  +-------------|     |     |     Handler     |
+--------------+    |                      |     +-----------------+
                    |                      |
                 
```

# Installation
- see ["interception_core_handler"](./interception_core_handler/README.md) directory for "Interception Core Handler"
- see ["interception_request_handler"](./interception_request_handler/README.md) directory for "Interception Request Handler"

# Configuration
- see ["interception_core_handler"](./interception_core_handler/README.md) directory for "Interception Core Handler"
- see ["interception_request_handler"](./interception_request_handler/README.md) directory for "Interception Request Handler"


# Usage
- see ["interception_core_handler"](./interception_core_handler/README.md) directory for "Interception Core Handler"
- see ["interception_request_handler"](./interception_request_handler/README.md) directory for "Interception Request Handler"