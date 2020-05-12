"""
configurationManager

developed by @Infocom - 2020
info: guerino.lamanna@infocomgenova.it
"""

import json
import logging
from myLogger import MyLogger

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
        self.tcpServerParams = {} # "address" and "port"
        self.kafkaServerParams = {} # "address", "port" and "topic"

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
            tcpServer = parameters.get( "tcpServer", "" )
            if tcpServer != "" :
                self.tcpServerParams[ "address" ] = tcpServer.get( "address", "" )
                self.tcpServerParams[ "port" ] = tcpServer.get( "port", "" )
                self.logger.debug( "TCP server address: %s, port: %s",
                    str( self.tcpServerParams[ "address" ] ),
                    str( self.tcpServerParams[ "port" ] ) )
            kafkaServer = parameters.get( "kafkaServer", "" )
            if kafkaServer != "" :
                self.kafkaServerParams[ "address" ] = kafkaServer.get( "address", "" )
                self.kafkaServerParams[ "port" ] = kafkaServer.get( "port", "" )
                self.kafkaServerParams[ "topic" ] = kafkaServer.get( "topic", "" )
                self.logger.debug( "Kafka server address: %s, port: %s, topic: %s",
                    str( self.kafkaServerParams[ "address" ] ),
                    str( self.kafkaServerParams[ "port" ] ),
                    str( self.kafkaServerParams[ "topic" ] ) )
        return None

    def getLoggerLevel( self ) :
        return self.loggerLevel

    def getTcpServerAddress( self ) :
        return self.tcpServerParams[ "address" ]

    def getTcpServerPort( self ) :
        return self.tcpServerParams[ "port" ]

    def getKafkaServerAddress( self ) :
        return self.kafkaServerParams[ "address" ]

    def getKafkaServerPort( self ) :
        return self.kafkaServerParams[ "port" ]

    def getKafkaServerTopic( self ) :
        return self.kafkaServerParams[ "topic" ]
