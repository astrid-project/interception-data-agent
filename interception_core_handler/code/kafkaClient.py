"""
kafkaClient

developed by @Infocom - 2020
info: guerino.lamanna@infocomgenova.it
"""

import json
import threading

from kafka import KafkaConsumer
from myLogger import MyLogger
from interceptionTask import InterceptionTask

class KafkaClient( threading.Thread ) :
    def __init__( self, address, port, topic,
            polycubeServerAddress, polycubeServerPort, interceptionInterfaceName,
            logVoIPFilePath, logVoIPFileName, readVoIPLogTimeout, 
            interceptionTool, savedInterceptionPath,
            logstashAddress, logstashMsgPort, logstashVersion,
            interceptionSenderTopic, logstashDataPort,
            tcpServerAddress, tcpServerPort  ) :
        self.address = address
        self.port = port
        self.topic = topic
        # value to stop KafkaClient run cycle
        self.live = True

        self.interceptionTasks = {}
        self.polycubeServerAddress = polycubeServerAddress
        self.polycubeServerPort = polycubeServerPort
        self.interceptionInterfaceName = interceptionInterfaceName
        self.logVoIPFilePath = logVoIPFilePath
        self.logVoIPFileName = logVoIPFileName
        self.readVoIPLogTimeout = readVoIPLogTimeout
        self.interceptionTool = interceptionTool
        self.savedInterceptionPath = savedInterceptionPath
        self.logstashAddress = logstashAddress
        self.logstashMsgPort = logstashMsgPort
        self.logstashVersion = logstashVersion
        self.interceptionSenderTopic = interceptionSenderTopic
        self.logstashDataPort = logstashDataPort
        self.tcpServerAddress = tcpServerAddress
        self.tcpServerPort = tcpServerPort

        myLogger = MyLogger()
        self.logger = myLogger.getLogger( __name__ )

        bootstrap_servers = [ str( self.address ) + ":" + str( self.port ) ]
        self.logger.debug( "kafka bootstrap server : %s", str( bootstrap_servers ) )

        # parameter to use at python restart
        auto_offset_reset = "earliest"
        # commit the read of message to kafka broker
        enable_auto_commit = True
        auto_commit_interval_ms = 1000
        group_id = "interception"
        value_deserializer = lambda x: json.loads( x.decode( 'utf-8' ) )

        self.consumer = KafkaConsumer( self.topic, bootstrap_servers = bootstrap_servers, auto_offset_reset = auto_offset_reset, enable_auto_commit = enable_auto_commit, group_id = group_id, value_deserializer = value_deserializer )

    #def receive( self ) :
    #    data = []
    #    for message in self.consumer :
    #        data.append( message.value )
    #        self.logger.debug( "receive from kafka: %s", str( message.value ) )
    #    return data

    def run( self ) :
        self.logger.debug( "kafka client receiver start" )
        while self.live :
            self.logger.debug( "wait for a message from kafka broker..." ) 
            #messages = self.receive()
            #for message in messages :
            for data in self.consumer :
                message = data.value
                self.logger.debug( "receive from kafka: %s", str( message ) )
                userID = message.get( "userID", "" )
                providerID = message.get( "providerID", "" )
                serviceID = message.get( "serviceID", "" )
                action = message.get( "action", "" )
                self.logger.debug( "%s, %s, %s, %s", userID, providerID, serviceID, action )

                if userID == "" or action == "" :
                    continue

                if action == "start" :
                    interceptionName = str( serviceID ) + str( providerID ) + str( userID )
            
                    if self.interceptionTasks.get( interceptionName, False ) :
                        self.logger.debug( "interception task yet exist !" )
                    else :
                        interceptionTask = InterceptionTask( userID, providerID, serviceID, 
                            self.polycubeServerAddress, self.polycubeServerPort, 
                            self.interceptionInterfaceName, self.logVoIPFilePath, 
                            self.logVoIPFileName, self.readVoIPLogTimeout,
                            self.interceptionTool,
                            self.savedInterceptionPath,
                            self.logstashAddress,
                            self.logstashMsgPort,
                            self.logstashVersion,
                            self.address,
                            self.port,
                            self.interceptionSenderTopic,
                            self.logstashDataPort,
                            self.tcpServerAddress,
                            self.tcpServerPort )
                        interceptionTask.start()
                        self.interceptionTasks[ interceptionName ] = interceptionTask

                if action == "stop" :
                    interceptionName = str( serviceID ) + str( providerID ) + str( userID )
                    interceptionTask = self.interceptionTasks.pop( interceptionName, False )
                    if interceptionTask :
                        interceptionTask.stop()
                        
                

