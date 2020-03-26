#!/bin/bash

# variables to set in configuration file
# here default values
logger_level="DEBUG"
interface=""
interception_path="./interceptions/"
rest_server_address="0.0.0.0"
rest_server_port=5003
polycube_address="127.0.0.1"
polycube_port=9000
kafka_address=""
kafka_port=5002
log_voip_path="./"
log_voip_file_name="containersLogs.log"
log_voip_reading_time=0.5
polycube_is_enabled=false
libpcap_is_enabled=true

help() {
    echo "Usage : "
    echo "-h                    Display this message"
    echo "-d DEBUG_LEVEL        Debug level: INFO, WARN, DEBUG (default), ERROR"
    echo "-i INTERFACE          Interface used to capture VoIP traffic, "
    echo "                          empty value (default) is for \"all interfaces\""
    echo "-p PATH               Path where interceptions are saved"
    echo "-a REST_IP            IP address of local REST listen server, "
    echo "                          default \"0.0.0.0\", all addresses"
    echo "-b REST_PORT          Port of local REST listen server, default 5003"
    echo "-e POLYCUBE_IP        Local Polycube IP address, default \"127.0.0.1\""
    echo "-f POLYCUBE_PORT      Local Polycube port, default 9000"
    echo "-g KAFKA_IP           Kafka IP address, default is empty value, not used"
    echo "-k KAFKA_PORT         Kafka port, default is 5002"
    echo "-m LOG_PATH           Path of VoIP log file (folder)"
    echo "-p LOG_FILENAME       Name of VoIP log file"
    echo "-t LOG_READ_TIME      Timeout for execution of one VoIP log file reading cycle"
    echo "-u ENABLE_POLYCUBE    Enable/disable Polycube PacketCapture for interception,"
    echo "                          allowed values: true (active) / false (deactive - default)"
    echo "-z ENABLE_LIBPCAP     Enable/disable Libpcap for interception,"
    echo "                          allowed values: true (active - default) / false (deactive)"
    echo ""
    echo "* If not specified, default value is used*"
    echo ""
}
# load data from parameters
while getopts ":hd:i:p:a:b:e:f:g:k:m:p:t:u:z:" args; do
    case ${args} in
        h)
            help
            ;;
        d) 
            logger_level=$OPTARG
            ;;
        i) 
            interface=$OPTARG
            ;;
        p) 
            interception_path=$OPTARG
            ;;
        a) 
            rest_server_address=$OPTARG
            ;;
        b) 
            rest_server_port=$OPTARG
            ;;
        e) 
            polycube_address=$OPTARG
            ;;
        f) 
            polycube_port=$OPTARG
            ;;
        g) 
            kafka_address=$OPTARG
            ;;
        k) 
            kafka_port=$OPTARG
            ;;
        m) 
            log_voip_path=$OPTARG
            ;;
        p) 
            log_voip_file_name=$OPTARG
            ;;
        t) 
            log_voip_reading_time=$OPTARG
            ;;
        u) 
            polycube_is_enabled=$OPTARG
            ;;
        z)  
            libpcap_is_enabled=$OPTARG
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
    sed -i "s#\@INTERFACE#${interface}#" ./config/configurationFile.conf
    sed -i "s#\@INTERCEPTIONPATH#${interception_path}#" ./config/configurationFile.conf
    sed -i "s#\@RESTSERVERADDRESS#${rest_server_address}#" ./config/configurationFile.conf
    sed -i "s#\@RESTSERVERPORT#${rest_server_port}#" ./config/configurationFile.conf
    sed -i "s#\@POLYCUBEADDRESS#${polycube_address}#" ./config/configurationFile.conf
    sed -i "s#\@POLYCUBEPORT#${polycube_port}#" ./config/configurationFile.conf
    sed -i "s#\@KAFKAADDRESS#${kafka_address}#" ./config/configurationFile.conf
    sed -i "s#\@KAFKAPORT#${kafka_port}#" ./config/configurationFile.conf
    sed -i "s#\@LOGVOIPPATH#${log_voip_path}#" ./config/configurationFile.conf
    sed -i "s#\@LOGVOIPFILENAME#${log_voip_file_name}#" ./config/configurationFile.conf
    sed -i "s#\@LOGVOIPREADINGTIME#${log_voip_reading_time}#" ./config/configurationFile.conf
    sed -i "s#\@POLYCUBEISENABLED#${polycube_is_enabled}#" ./config/configurationFile.conf
    sed -i "s#\@LIBPCAPISENABLED#${libpcap_is_enabled}#" ./config/configurationFile.conf
else
    echo "Error: ./config/base.conf does not exist"
    exit 1
fi

exit 0



