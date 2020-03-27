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
            configFilePath = "./" 
        ):
        self.logger = ""
        self.configFileName = configFileName
        self.configFilePath = configFilePath
        self.jsonDictionary = {}
        
        # buffer to save configuration parameters 
        self.loggerLevel = logging.DEBUG
        self.restServerParams = {} # "address" and "port"
        self.contextBrokerParams = {} # "address" and "port"

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
            restServer = parameters.get( "restServer", "" )
            if restServer != "" :
                self.restServerParams[ "address" ] = restServer.get( "address", "" )
                self.restServerParams[ "port" ] = restServer.get( "port", "" )
                self.logger.debug( "REST server address: %s, port: %s", 
                    str( self.restServerParams[ "address" ] ), 
                    str( self.restServerParams[ "port" ] ) )
            contextBroker = parameters.get( "contextBroker", "" )
            if contextBroker != "" :
                self.contextBrokerParams[ "address" ] = contextBroker.get( "address", "" )
                self.contextBrokerParams[ "port" ] = contextBroker.get( "port", "" )
                self.logger.debug( "ContextBroker server address: %s, port: %s", 
                    str( self.contextBrokerParams[ "address" ] ), 
                    str( self.contextBrokerParams[ "port" ] ) )
        return None

    def getLoggerLevel( self ) :
        return self.loggerLevel

    def getRestServerAddress( self ) :
        return self.restServerParams[ "address" ]

    def getRestServerPort( self ) :
        return self.restServerParams[ "port" ]

    def getContextBrokerAddress( self ) :
        return self.contextBrokerParams[ "address" ]

    def getContextBrokerPort( self ) :
        return self.contextBrokerParams[ "port" ]
