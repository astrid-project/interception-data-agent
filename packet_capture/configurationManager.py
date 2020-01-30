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
        self.packetInterceptionParameters = None
        self.logServerParameters = None

        try:
            path = self.configFilePath + self.configFileName
            with open( path ) as jsonFile :
                self.jsonDictionary = json.load( jsonFile )
        except FileNotFoundError as exception:
            logger.debug( exception )

        if "parameters" in self.jsonDictionary :
            parameters = self.jsonDictionary[ "parameters" ]
            if "packetInterception" in parameters :
                self.packetInterceptionParameters = parameters[ "packetInterception" ]
            if "logServer" in parameters :
                self.logServerParameters = parameters[ "logServer" ]

        return None

    def getPacketInterceptionAddress( self ) :
        if "address" in self.packetInterceptionParameters :
            return self.packetInterceptionParameters[ "address" ]
        return None

    def getPacketInterceptionPort( self ) :
        if "port" in self.packetInterceptionParameters :
            return self.packetInterceptionParameters[ "port" ]
        return None

    def getLogServerAddress( self ) :
        if "address" in self.logServerParameters :
            return self.logServerParameters[ "address" ]
        return None

    def getLogServerPort( self ) :
        if "port" in self.logServerParameters :
            return self.logServerParameters[ "port" ]
        return None