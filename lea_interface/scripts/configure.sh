#!/bin/bash

# variables to set in configuration file
# here default values
logger_level="DEBUG"
tcp_server_address="0.0.0.0"
tcp_server_port=5004
kafka_address=""
kafka_port=5002
kafka_topic="interception"

help() {
    echo "Usage : "
    echo "-h                    Display this message"
    echo "-d DEBUG_LEVEL        Debug level: INFO, WARN, DEBUG (default), ERROR"
    echo "-t TCP_IP             IP address of local TCP listen server, "
    echo "                          default \"0.0.0.0\", all addresses"
    echo "-u TCP_PORT           Port of local TCP listen server, default 5004"
    echo "-g KAFKA_IP           Kafka IP address, default is empty value, not used"
    echo "-k KAFKA_PORT         Kafka port, default is 5002"
    echo "-w KAFKA_TOPIC        Kafka topic used for communication with Kafka broker"
    echo ""
    echo "* If not specified, default value is used *"
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
        t)
            tcp_server_address=$OPTARG
            ;;
        u)
            tcp_server_port=$OPTARG
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
    sed -i "s#\@TCPSERVERADDRESS#${tcp_server_address}#" ./config/configurationFile.conf
    sed -i "s#\@TCPSERVERPORT#${tcp_server_port}#" ./config/configurationFile.conf
    sed -i "s#\@KAFKAADDRESS#${kafka_address}#" ./config/configurationFile.conf
    sed -i "s#\@KAFKAPORT#${kafka_port}#" ./config/configurationFile.conf
    sed -i "s#\@KAFKATOPIC#${kafka_topic}#" ./config/configurationFile.conf
else
    echo "Error: ./config/base.conf does not exist"
    exit 1
fi

exit 0