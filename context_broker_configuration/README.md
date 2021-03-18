# ContextBroker use guide for Interception Core Handler

The ContextBroker is used to configure the "Interception Core Handler" (that is classified as an agent in Astrid framework) and start/stop interception streams.


We can identify two types of REST API calls: starting configuration and interception managing.


## Starting configuration

At the startup of the system, it is important to configure the Astrid framework to use "Interception Core Handler" agent.
To do this we need to follow two steps:

* Define "Interception Core Handler" agent in the Astrid Agents Catalog.
  REST API: POST -> Context-Broker-IP:5000/exec-env
  [Payload](./execenv_post_payload.json):

```
[
  {
    "lcp": {
		"port": 4000
    },
    "id": "interception-core-handler", // define unique ID for the Execution Environment instance
    "description": "Interception Core Handler",
    "type_id": "container-docker", // type of Execution Environment
    "hostname": "interception-core-handler.interception", // in our example "interception" is the namespace and "interception-core-handler" the name of the POD
    "enabled": "Yes"
  }
]
```

* Create the instance of the Execution Environment ("Interception Core Handler" POD)
  REST API: POST -> Context-Broker-IP:5000/catalog/agent
  [Payload](./catalog_agent_post_payload.json):

```
[
	{
		"id": "interception-core-agent", // define unique ID for the "Interception Core Handler" agent
		"actions": [
			{
				"id": "start",
				"status": "started",
				"config": {
					"cmd": "curl localhost:5003/interceptionstart -d '{\"userID\":\"{userID}\", \"serviceProviderID\":\"{serviceProviderID}\",  \"serviceID\": \"{serviceID}\"}'"
				}
			},
			{
				"id": "stop",
				"status": "stopped",
				"config": {
					"cmd": "curl localhost:5003/interceptionstop -d '{\"userID\":\"{userID}\", \"serviceProviderID\":\"{serviceProviderID}\",  \"serviceID\": \"{serviceID}\"}'"
				}
			}
		]
	}
]
```

## Interception managing

After the creation of the Execution Environment and definition of the agent in the Astrid Catalog, it is possibile to use the Context Broker to start/stop the interception stream.

WARNING: only the first time it is important to create the instance of the interception agent (that start the interception stream) by POST method.
After that, it is possibile start/stop the interception stream modifying parameters in the interception agent instance, so it is possible to use only the PUT methods.

* Create instance of the agent and start the interception
  REST API: POST -> Context-Broker-IP:5000/instance/agent
  [Payload](./instance_agent_post_payload.json):

```
[
	{
		"id": "interception-core-agent@interception-core-handler", // define unique ID for the agent instance
		"agent_catalog_id": "interception-core-agent", // name of the agent in the Astrid Catalog
		"exec_env_id": "interception-core-handler", // name of the Execution Environment
		"description": "Instance of Interception Core Agent",
		"status": "started",
		"operations": {
			"actions": [
				{
					"id": "start",
					"userID":  "+306944125708",
					"serviceProviderID": "2",
					"serviceID": "3"
				}
			]
		}
	}
]
```

* Modify an existing agent instance to start the interception
  REST API: PUT -> Context-Broker-IP:5000/instance/agent
  [Payload](./instance_agent_start_put_payload.json):

```
[
	{
		"id": "interception-core-agent@interception-core-handler", // use the same ID of the agent instance
		"description": "Instance of Interception Core Agent",
		"operations": {
			"actions": [
				{
					"id": "start",
					"userID":  "@USERID", // change @USERID with the user Id
					"serviceProviderID": "@PROVIDERID", // change @PROVIDERID with provider Id
					"serviceID": "@SERVICEID" // change @SERVICEID with service Id
				}
			]
		}
	}
]
```

* Modify an existing agent instance to stop the interception
  REST API: PUT -> Context-Broker-IP:5000:/instance/agent
  [Payload](./instance_agent_stop_put_payload.json):

```
[
	{
		"id": "interception-core-agent@interception-core-handler", // use the same ID of the agent instance
		"description": "Instance of Interception Core Agent",
		"operations": {
			"actions": [
				{
					"id": "stop",
					"userID":  "@USERID", // change @USERID with the user Id
					"serviceProviderID": "@PROVIDERID", // change @PROVIDERID with the provider Id
					"serviceID": "@SERVICEID" // change @SERVICEID with the service Id
				}
			]
		}
	}
]
```



