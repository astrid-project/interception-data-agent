"""
configurationManager

developed by @Infocom - 2020
info: guerino.lamanna@infocomgenova.it
"""

import json
import logging
from myLogger import MyLogger
from enum import Enum

class InterceptionTool( Enum ) :
    Undefined = 0
    PolycubePacketCapture = 1
    Tcpdump = 2

class ConfigurationManager():
    """
    Configuration Manager is used to manage the configuration parameters.
    It read configuration file and load data into the program.
    The configuration file is loaded only on code starting
    ::
    Parameters: 
    ::
    configFileName -- name of config file. 
                        Default value: "configurationFile.conf" 
    ::
    configFilePath -- relative/absolute path where config file is.
                        Default value: "./" 
    """
    def __init__( 
            self, 
            configFileName = "configurationFile.conf",
            configFilePath = "./config/" 
        ):
        self.logger = ""
        self.configFileName = configFileName
        self.configFilePath = configFilePath
        self.jsonDictionary = {}
        
        # buffer to save configuration parameters 
        self.loggerLevel = logging.DEBUG
        self.interceptionInterfaceName = ""
        self.savedInterceptionPath = ""
        self.restServerParams = {} # "address" and "port"
        self.polycubeServerParams = {} # "address" and "port"
        self.kafkaServerParams = {} # "address" and "port"
        self.logstashServerParams = {} # "address", "msgPort", "dataPort" and "version"
        self.logVoIPServerParams = {} # "path" and "timeout"
        self.interceptionTool = ""
        self.tcpServerParams = {} # "address" and "port"

        try:
            path = self.configFilePath + self.configFileName
            with open( path ) as jsonFile :
                self.jsonDictionary = json.load( jsonFile )
        except FileNotFoundError as exception:
            if self.logger :
                self.logger.error( exception )
            else :
                print( exception )

        parameters = self.jsonDictionary.get( "parameters", "" )
        if parameters != "" :
            loggerLevel = parameters.get( "loggerLevel", "" )
            if loggerLevel != "" :
                if loggerLevel == "INFO" :
                    self.loggerLevel = logging.INFO
                if loggerLevel == "WARN" :
                    self.loggerLevel = logging.WARN
                if loggerLevel == "DEBUG" :
                    self.loggerLevel = logging.DEBUG
                if loggerLevel == "ERROR" :
                    self.loggerLevel = logging.ERROR
                myLogger = MyLogger()
                myLogger.setLogLevel( self.loggerLevel)
                self.logger = myLogger.getLogger( __name__ )
                self.logger.debug( "logLevel: %s", str( self.loggerLevel ) )
            self.interceptionInterfaceName = parameters.get( "interceptionInterfaceName", "" )
            self.logger.debug( "interception interface name: %s", str( self.interceptionInterfaceName ) )
            self.savedInterceptionPath = parameters.get( "savedInterceptionPath", "" )
            self.logger.debug( "saved interceptions path : %s", str( self.savedInterceptionPath ) )
            restServer = parameters.get( "restServer", "" )
            if restServer != "" :
                self.restServerParams[ "address" ] = restServer.get( "address", "" )
                self.restServerParams[ "port" ] = restServer.get( "port", "" )
                self.logger.debug( "REST server address: %s, port: %s", 
                    str( self.restServerParams[ "address" ] ), 
                    str( self.restServerParams[ "port" ] ) )
            polycubeServer = parameters.get( "polycubeServer", "" )
            if polycubeServer != "" :
                self.polycubeServerParams[ "address" ] = polycubeServer.get( "address", "" )
                self.polycubeServerParams[ "port" ] = polycubeServer.get( "port", "" )
                self.logger.debug( "Polycube address: %s, port: %s",
                    str( self.polycubeServerParams[ "address" ] ),
                    str( self.polycubeServerParams[ "port" ] ) )
            kafkaServer = parameters.get( "kafkaServer", "" )
            if kafkaServer != "" :
                self.kafkaServerParams[ "address" ] = kafkaServer.get( "address", "" )
                self.kafkaServerParams[ "port" ] = kafkaServer.get( "port", "" )
                self.kafkaServerParams[ "topic" ] = kafkaServer.get( "topic", "" )
                self.logger.debug( "Kafka server address: %s, port: %s, topic: %s",
                    str( self.kafkaServerParams[ "address" ] ),
                    str( self.kafkaServerParams[ "port" ] ),
                    str( self.kafkaServerParams[ "topic" ] ) )
            logstashServer = parameters.get( "logstashServer", "" )
            if logstashServer != "" :
                self.logstashServerParams[ "address" ] = logstashServer.get( "address", "" )
                self.logstashServerParams[ "msgPort" ] = logstashServer.get( "msgPort", "" )
                self.logstashServerParams[ "dataPort" ] = logstashServer.get( "dataPort", "" )
                self.logstashServerParams[ "version" ] = logstashServer.get( "version", "" )
                self.logger.debug( "Logstash server address: %s, msgPort: %s, dataPort: %s, version: %s",
                    str( self.logstashServerParams[ "address" ] ),
                    str( self.logstashServerParams[ "msgPort" ] ),
                    str( self.logstashServerParams[ "dataPort" ] ),
                    str( self.logstashServerParams[ "version" ] ))
            logVoIPServer = parameters.get( "logVoIPServer", "" )
            if logVoIPServer != "" :
                self.logVoIPServerParams[ "path" ] = logVoIPServer.get( "path", "" )
                self.logVoIPServerParams[ "name" ] = logVoIPServer.get( "name", "" )
                self.logVoIPServerParams[ "readingTimeOut" ] = logVoIPServer.get( "readingTimeOut", 0.5 )
                self.logger.debug( "log VoIP server path: \"%s\", file name: \"%s\", reading timeout: %s sec",
                    str( self.logVoIPServerParams[ "path" ] ), str( self.logVoIPServerParams[ "name" ] ),
                    str( self.logVoIPServerParams[ "readingTimeOut" ] ) )
            tcpServer = parameters.get( "tcpServer", "" )
            if tcpServer != "" :
                self.tcpServerParams[ "address" ] = tcpServer.get( "address", "" )
                self.tcpServerParams[ "port" ] = tcpServer.get( "port", "" )
                self.logger.debug( "tcp server address: %s, port: %s", \
                    str( self.tcpServerParams[ "address" ] ), str( self.tcpServerParams[ "port" ] ) )
            interceptionTool = parameters.get( "interceptionTool", "" )
            if interceptionTool != "" :
                isPolycubePacketCaptureEnabled = interceptionTool.get( "polycubePacketCapture", False )
                isTcpdumpEnabled = interceptionTool.get( "libpcap" , False )
                if isPolycubePacketCaptureEnabled :
                    self.logger.debug( "interception tool is set to be Polycube Packetcapture" )
                    self.interceptionTool = InterceptionTool.PolycubePacketCapture
                if isTcpdumpEnabled :
                    self.logger.debug( "interception tools is set to be Tcpdump" )
                    self.interceptionTool = InterceptionTool.Tcpdump
                if isPolycubePacketCaptureEnabled and isTcpdumpEnabled :
                    self.logger.error( "yet Polycube Packetcapture and Tcpdump are set to be enabled" )
                    raise Exception( "yet Polycube Packetcapture and Tcpdump are set to be enabled" )
                if isPolycubePacketCaptureEnabled == False and isTcpdumpEnabled == False :
                    self.logger.error( "yet Polycube Packetcapture and Tcpdump are set do be DISABLED" )
                    raise Exception( "yet Polycube Packetcapture and Tcpdump are set do be DISABLED" )
        return None

    def getLoggerLevel( self ) :
        return self.loggerLevel

    def getInterceptionInterfaceName( self ) :
        return self.interceptionInterfaceName

    def getSavedInterceptionPath( self ) :
        return self.savedInterceptionPath

    def getRestServerAddress( self ) :
        return self.restServerParams[ "address" ]

    def getRestServerPort( self ) :
        return self.restServerParams[ "port" ]

    def getPolycubeServerAddress( self ) :
        return self.polycubeServerParams[ "address" ]

    def getPolycubeServerPort( self ) :
        return self.polycubeServerParams[ "port" ]

    def getKafkaServerAddress( self ) :
        return self.kafkaServerParams[ "address" ]
    
    def getKafkaServerPort( self ) :
        return self.kafkaServerParams[ "port" ]

    def getKafkaServerTopic( self ) :
        return self.kafkaServerParams[ "topic" ]

    def getLogstashServerAddress( self ) :
        return self.logstashServerParams[ "address" ]

    def getLogstashServerMsgPort( self ) :
        return self.logstashServerParams[ "msgPort" ]

    def getLogstashServerDataPort( self ) :
        return self.logstashServerParams[ "dataPort" ]

    def getLogstashServerVersion( self ) :
        return self.logstashServerParams[ "version" ]

    def getLogVoIPServerPath( self ) :
        return self.logVoIPServerParams[ "path" ]

    def getLogVoIPServerFilename( self ) :
        return self.logVoIPServerParams[ "name" ]

    def getVoIPLogReadingTimeOut( self ) :
        return self.logVoIPServerParams[ "readingTimeOut" ]

    def getTcpServerAddress( self ) :
        return self.tcpServerParams[ "address" ]

    def getTcpServerPort( self ) :
        return self.tcpServerParams[ "port" ] 

    def getInterceptionTool( self ) :
        return self.interceptionTool
