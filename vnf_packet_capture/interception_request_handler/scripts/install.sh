#!/bin/bash

# variables to set in configuration file
# here default values
logger_level:="DEBUG"
rest_server_address:="0.0.0.0"
rest_server_port:=5003
polycube_address:="127.0.0.1"
polycube_port:=9000
contextbroker_address:=""
contextbroker_port:=""
contextbroker_user:="astrid"
contextbroker_password:=""

help() {
    echo "Usage : "
    echo "-h                    Display this message"
    echo "-d DEBUG_LEVEL        Debug level: INFO, WARN, DEBUG (default), ERROR"
    echo "-a REST_IP            IP address of local REST listen server, "
    echo "                          default \"0.0.0.0\", all addresses"
    echo "-b REST_PORT          Port of local REST listen server, default 5003"
    echo "-e CONTEXTBROKER_IP   Local ContextBroker IP address, default value is empty"
    echo "-f CONTEXTBROKER_PORT Local ContextBroker port, default value is empty"
    echo "-u USER               User to use to connect to ContextBroker, default value is \"astrid\""
    echo "-p PASSWORD           Password to use to connect to ContextBroker"
    echo ""
    echo "* If not specified, default value is used*"
    echo ""
    exit $1
}
# load data from parameters
while getopts ":hd:i:p:a:b:e:f:u:p:" opt; do
    case ${args} in
        h )
            help 0
            ;;
        d ) 
            logger_level = $OPTARG
            ;;
        a ) 
            rest_server_address = $OPTARG
            ;;
        b ) 
            rest_server_port = $OPTARG
            ;;
        e ) 
            contextbroker_address = $OPTARG
            ;;
        f ) 
            contextbroker_port = $OPTARG
            ;;
        u ) 
            contextbroker_user = $OPTARG
            ;;
        p ) 
            contextbroker_password = $OPTARG
            ;;
        \? )
            echo "Error: Invalid argument : ${args}"
            echo ""
            help 1
            ;;
        : )
            echo "Error: $OPTARG requires argument"
            echo ""
            help 1
            ;;
    esac
done

# check if python3
if [ ! $(type -p python3) ]; then
    echo "Error: \"python3\" not found"
    echo ""
    exit 1
fi

# check if pip3 exist and execute pip3 requirements
if [ ! $(type -p pip3) ]; then
    echo "Error: \"pip3\" not found"
    echo ""
    exit 1
else
    pip3 install -r ./scripts/requirements.txt
fi

# download git repository
if [ ! -d .git ]; then
    echo Clone repository
    rm -rf env/lcp
    git clone https://astrid-dev:PDskARWrfWHSxJtk9yzQ@gitlab.com/astrid-repositories/wp2/interception-data-agent.git
else
    echo Pull repository
    git pull origin master
fi


# fill parameters in configuration file
if [ -f ./config/base.conf ]; then
    cp ./config/base.conf .config/configurationFile.conf
    sed -i 's/\@LOGGERLEVEL/${logger_level}' ./config/configurationfile.conf
    sed -i 's/\@RESTSERVERADDRESS/${rest_server_address}' ./config/configurationfile.conf
    sed -i 's/\@RESTSERVERPORT/${rest_server_port}' ./config/configurationfile.conf
    sed -i 's/\@CONTEXTBROKERADDRESS/${contextbroker_address}' ./config/configurationfile.conf
    sed -i 's/\@CONTEXTBROKERPORT/${contextbroker_port}' ./config/configurationfile.conf
    sed -i 's/\@CONTEXTBROKERUSER/${contextbroker_user}' ./config/configurationfile.conf
    sed -i 's/\@CONTEXTBROKERPASSWORD/${contextbroker_password}' ./config/configurationfile.conf
else
    echo "Error: ./config/base.conf does not exist"
    exit 1






