# Elastic suite 
"Elastic suite" is used to move interception information (start call, missing call, etc) and interception capture from "Execution Environment" (VM - Virtual Machine) to the LEA.

This goal is achieved by a directly TCP connection or using "Elastic Suite". 

Here we see the latter case.

# Kafka
"Kafka" software is the "messaging broker". "Interception Data Agent" uses "Kafka" to send data (call information and interceptions) to Astrid border, where, by a specific interface, LEA can get them.

"Kafka" uses two topics, that, in the default configuration, are "interception" and "interception_data". It is possible to modify these labels by "Interception Data Agent" file configuration.

In the basic configuration, shown in this tutorial, "Kafka" is not used. 

## Table of content
- [Description of the case](#description-of-the-case)
- [Configuration](#configuration)
- [Installation](#installation)


# Description of the case
The configuration, used in this case, is very easy. Only one instance of "Logstash" is deployed, which requests two pipeline: one to save information data about calls and another to save call interceptions.

Both pipelines are defined to save input in different files, as shown in figure below.

```
 
 +--------------+       
 | Interception |       +----------+         +--------+     +--------+
 | Core Handler | --->  | Logstash |  ---->  | File-1 | ... | File-n | (Calls information)
 +--------------|       +----------+         +--------+     +--------+
                              |              +--------+     +--------+ 
                              +----------->  | File-1 | ... | File-n | (Calls interception)
                                             +--------+     +--------+

```

# Configuration
Every pipeline has a different configuration file (folder: /etc/logstash/conf.d/):
- logstash_for_call_information.conf

This pipeline receives calls information data from a specific port (in JSON format) and write them on a specific folder (name of file is dynamic defined from ID of the intercepted user).

```python
# wait message from port 5959
input {
  tcp {
    port => 5959
    codec => json
  }
}

# write output on /tmp/ folder with a dinamyc name
output {
  file {
     path => "/tmp/interception_messages_%{userid}.json"
     #codec => line { format => "%{message}" }
     codec => rubydebug
  }
}
```

- logstash_for_interception_saving.conf 

"Logstash" used a specific pipeline to save VoIP interception data. The first part create a server listening to specific port to receive interception stream data. Then "Ruby" filter decode traffic and save it in a specific file (name of this file is dynamic and depend on the interception data).
At last  
```python
# receive message from 5960 port
input {
  tcp {
    port => 5960
    codec => json
  }
}

# decode message and save interception in /tmp/ folder
filter {
  ruby {
     init => 'require "base64"'
     code => 'event.set("data", Base64.decode64(event.get("data")));
              data = event.get("data");
              path = "/tmp/interception_data_";
              path.concat( event.get("interceptionfilename") );
              File.open(path, "ab") {|file| file.write( data ) };'
  }
}

# write all messages on /tmp/ folder, only for DEBUG purpose
output {
  file {
     path => "/tmp/interception_pure.pcap"
     codec => rubydebug
  }
}
```


# Installation
"Logstash" configuration relies on creation of two pipelines. To do this, modify "pipelines.yml" file, adding following lines:

``` yml
- pipeline.id: call_info
  path.config: "/etc/logstash/conf.d/logstash_for_call_information.conf"
- pipeline.id: call_interception
  path.config: "/etc/logstash/conf.d/logstash_for_interception_saving.conf"
```

Then copy configuration files ("logstash_for_call_information.conf" and "logstash_for_interception_saving.conf") in the folder "/etc/logstash/conf.d/".




