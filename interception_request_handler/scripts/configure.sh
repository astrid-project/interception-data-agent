#!/bin/bash

# variables to set in configuration file
# here default values
logger_level="DEBUG"
rest_server_address="0.0.0.0"
rest_server_port=5003
kafka_address=""
kafka_port=5002
kafka_topic="interception"
contextbroker_address=""
contextbroker_port=0
contextbroker_user="astrid"
contextbroker_password=""

help() {
    echo "Usage : "
    echo "-h                    Display this message"
    echo "-d DEBUG_LEVEL        Debug level: INFO, WARN, DEBUG (default), ERROR"
    echo "-a REST_IP            IP address of local REST listen server, "
    echo "                          default \"0.0.0.0\", all addresses"
    echo "-b REST_PORT          Port of local REST listen server, default 5003"
    echo "-g KAFKA_IP           Kafka IP address, default is empty value, not used"
    echo "-k KAFKA_PORT         Kafka port, default is 5002"
    echo "-w KAFKA_TOPIC        Kafka topic used for communication with Kafka broker"
    echo "-e CONTEXTBROKER_IP   Local ContextBroker IP address, default value is empty"
    echo "-f CONTEXTBROKER_PORT Local ContextBroker port, default value is empty"
    echo "-u USER               User to use to connect to ContextBroker, default value is \"astrid\""
    echo "-p PASSWORD           Password to use to connect to ContextBroker"
    echo ""
    echo "* If not specified, default value is used*"
    echo ""
}
# load data from parameters
while getopts ":hd:i:p:a:b:g:k:w:e:f:u:p:" args; do
    case ${args} in
        h)
            help
            ;;
        d) 
            logger_level=$OPTARG
            ;;
        a) 
            rest_server_address=$OPTARG
            ;;
        b) 
            rest_server_port=$OPTARG
            ;;
        g)
            kafka_address=$OPTARG
            ;;
        k)
            kafka_port=$OPTARG
            ;;
        w)
            kafka_topic=$OPTARG
            ;;
        e) 
            contextbroker_address=$OPTARG
            ;;
        f) 
            contextbroker_port=$OPTARG
            ;;
        u) 
            contextbroker_user=$OPTARG
            ;;
        p) 
            contextbroker_password=$OPTARG
            ;;
        \?)
            echo "Error: Invalid argument : ${args}"
            echo ""
            help
            exit 1
            ;;
        :)
            echo "Error: $OPTARG requires argument"
            echo ""
            help
            exit 1
            ;;
    esac
done

# download git repository
#if [ ! -d .git ]; then
#    echo Clone repository
#    rm -rf env/lcp
#    git clone https://astrid-dev:PDskARWrfWHSxJtk9yzQ@gitlab.com/astrid-repositories/wp2/interception-data-agent.git
#else
#    echo Pull repository
#    git pull origin master
#fi


# fill parameters in configuration file
if [ -f ./config/base.conf ]; then
    cp ./config/base.conf ./config/configurationFile.conf
    sed -i "s#\@LOGGERLEVEL#${logger_level}#" ./config/configurationFile.conf
    sed -i "s#\@RESTSERVERADDRESS#${rest_server_address}#" ./config/configurationFile.conf
    sed -i "s#\@RESTSERVERPORT#${rest_server_port}#" ./config/configurationFile.conf
    sed -i "s#\@KAFKAADDRESS#${kafka_address}#" ./config/configurationFile.conf
    sed -i "s#\@KAFKAPORT#${kafka_port}#" ./config/configurationFile.conf
    sed -i "s#\@KAFKATOPIC#${kafka_topic}#" ./config/configurationFile.conf
    sed -i "s#\@CONTEXTBROKERADDRESS#${contextbroker_address}#" ./config/configurationFile.conf
    sed -i "s#\@CONTEXTBROKERPORT#${contextbroker_port}#" ./config/configurationFile.conf
    sed -i "s#\@CONTEXTBROKERUSER#${contextbroker_user}#" ./config/configurationFile.conf
    sed -i "s#\@CONTEXTBROKERPASSWORD#${contextbroker_password}#" ./config/configurationFile.conf
else
    echo "Error: ./config/base.conf does not exist"
    exit 1
fi

exit 0