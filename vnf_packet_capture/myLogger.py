"""
myLogger

developed by @Infocom - 2020
info: guerino.lamanna@infocomgenova.it
"""

import logging

class MyLogger() :
    logLevel = ""
    formatter = "%(name)s - %(levelname)s - %(message)s"

    def setLogLevel( self, logLevel ) :
        MyLogger.logLevel = logLevel

    def getLogger( self, logName = __name__ ) :
        if MyLogger.logLevel :
            logger = logging.getLogger( logName )
            logHandler = logging.StreamHandler()
            logFormat = logging.Formatter( MyLogger.formatter )
            logHandler.setFormatter( logFormat )
            logger.addHandler( logHandler )
            logger.setLevel( MyLogger.logLevel )
            return logger
        return ""