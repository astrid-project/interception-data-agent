"""
configurationManager

developed by @Infocom - 2020
info: guerino.lamanna@infocomgenova.it
"""

import json
import logging

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
            configFilePath = "./" 
        ):
        self.logger = logging.getLogger( "mainLogger" )
        self.configFileName = configFileName
        self.configFilePath = configFilePath
        self.jsonDictionary = {}
        
        # buffer to save configuration parameters 
        self.loggerLevel = logging.DEBUG
        self.restServerParams = {} # "address" and "port"
        self.polycubeServerParams = {} # "address" and "port"
        self.kafkaServerParams = {} # "address" and "port"
        self.logServerParams = {} # "path"

        try:
            path = self.configFilePath + self.configFileName
            with open( path ) as jsonFile :
                self.jsonDictionary = json.load( jsonFile )
        except FileNotFoundError as exception:
            self.logger.debug( exception )

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
                self.logger.setLevel( self.loggerLevel )
            restServer = parameters.get( "restServer", "" )
            if restServer != "" :
                self.restServerParams[ "address" ] = restServer.get( "address", "" )
                self.restServerParams[ "port" ] = restServer.get( "port", "" )
            polycubeServer = parameters.get( "polycubeServer", "" )
            if polycubeServer != "" :
                self.polycubeServerParams[ "address" ] = polycubeServer.get( "address", "" )
                self.polycubeServerParams[ "port" ] = polycubeServer.get( "port", "" )
            kafkaServer = parameters.get( "kafkaServer")
            if kafkaServer != "" :
                self.kafkaServerParams[ "address" ] = kafkaServer.get( "address", "" )
                self.kafkaServerParams[ "port" ] = kafkaServer.get( "port", "" )
            logServer = parameters.get( "logServer" )
            if logServer != "" :
                self.logServerParams[ "path" ] = logServer.get( "path", "" )

        return None

    def getLoggerLevel( self ) :
        return self.loggerLevel

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

    def getLogServerPath( self ) :
        return self.logServerParams[ "path" ]

